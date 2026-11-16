#!/usr/bin/env python3
"""Installer generator and verification utility for Clarity Windows Distribution.

Usage:
    python installer/scripts/generate_installer.py [--validate] [--compile]
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import clarity

ISS_PATH = REPO_ROOT / "installer" / "windows" / "clarity_setup.iss"


def verify_version_alignment() -> str:
    """Verify that version strings in code, pyproject, and ISS are strictly aligned."""
    code_version = clarity.__version__

    # 1. Check pyproject.toml
    pyproject_path = REPO_ROOT / "pyproject.toml"
    if pyproject_path.exists():
        content = pyproject_path.read_text(encoding="utf-8")
        match = re.search(r'version\s*=\s*"([^"]+)"', content)
        if match and match.group(1) != code_version:
            raise ValueError(
                f"Version mismatch: clarity/__init__.py ({code_version}) vs pyproject.toml ({match.group(1)})"
            )

    # 2. Check Inno Setup script
    if ISS_PATH.exists():
        iss_content = ISS_PATH.read_text(encoding="utf-8")
        match = re.search(r'#define MyAppVersion "([^"]+)"', iss_content)
        if match and match.group(1) != code_version:
            raise ValueError(
                f"Version mismatch: clarity/__init__.py ({code_version}) vs clarity_setup.iss ({match.group(1)})"
            )

    print(f"[✓] Version alignment confirmed: v{code_version}")
    return code_version


def validate_installer_prerequisites() -> None:
    """Verify that all source files and paths expected by the installer exist."""
    print("[*] Validating installer prerequisites...")
    verify_version_alignment()

    if not ISS_PATH.exists():
        raise FileNotFoundError(f"Inno Setup script not found at {ISS_PATH}")

    dist_clarity = REPO_ROOT / "dist" / "clarity"
    if not dist_clarity.exists():
        print(f"[!] Warning: Standalone distribution directory {dist_clarity} does not exist yet.")
        print("    Run `python installer/scripts/build_standalone.py` to build the binary bundle.")
    else:
        print(f"[✓] Standalone distribution directory present at: {dist_clarity}")

    license_file = REPO_ROOT / "LICENSE"
    if not license_file.exists():
        raise FileNotFoundError(f"LICENSE file missing at {license_file}")

    examples_dir = REPO_ROOT / "examples"
    if not examples_dir.exists():
        raise FileNotFoundError(f"Examples directory missing at {examples_dir}")

    print("[✓] All installer prerequisite files verified successfully.")


def find_inno_compiler() -> str | None:
    """Locate Inno Setup compiler executable (ISCC.exe / iscc)."""
    # Check PATH
    iscc = shutil.which("iscc") or shutil.which("ISCC") or shutil.which("ISCC.exe")
    if iscc:
        return iscc

    # Check standard Windows paths
    candidates = [
        Path(r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe"),
        Path(r"C:\Program Files\Inno Setup 6\ISCC.exe"),
        Path(r"C:\Program Files (x86)\Inno Setup 5\ISCC.exe"),
    ]
    for c in candidates:
        if c.exists():
            return str(c)
    return None


def compile_installer() -> None:
    """Invoke Inno Setup compiler to build the final setup executable."""
    validate_installer_prerequisites()
    iscc = find_inno_compiler()

    if not iscc:
        print("[!] Inno Setup compiler (ISCC.exe) not found on this system.")
        print("    On Windows: Install Inno Setup 6 (https://jrsoftware.org/isdl.php).")
        print("    In CI/CD: The GitHub Actions workflow automatically provides ISCC.")
        print(f"    Script ready for compilation: {ISS_PATH}")
        return

    output_dir = REPO_ROOT / "dist" / "installer"
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"[*] Compiling installer using: {iscc}")
    cmd = [iscc, str(ISS_PATH)]
    res = subprocess.run(cmd, cwd=str(ISS_PATH.parent), check=False)
    if res.returncode != 0:
        raise RuntimeError(f"Inno Setup compilation failed with code {res.returncode}")

    print(f"[✓] Windows installer successfully compiled into: {output_dir}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate and validate Clarity Windows Installer.")
    parser.add_argument("--validate", action="store_true", help="Validate version alignment and prerequisites.")
    parser.add_argument("--compile", action="store_true", help="Compile the installer with Inno Setup if available.")
    args = parser.parse_args()

    try:
        if args.compile:
            compile_installer()
        else:
            validate_installer_prerequisites()
        return 0
    except Exception as exc:
        print(f"[!] Installer generation error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
