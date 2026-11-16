#!/usr/bin/env python3
"""Build standalone Clarity CLI distribution using PyInstaller.

Usage:
    python installer/scripts/build_standalone.py [--clean]
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

# Ensure repository root is on sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import clarity


def get_version() -> str:
    """Retrieve canonical Clarity version."""
    return clarity.__version__


def clean_build_artifacts() -> None:
    """Remove previous build and dist artifacts."""
    for path in [REPO_ROOT / "build" / "clarity", REPO_ROOT / "dist" / "clarity"]:
        if path.exists():
            print(f"[*] Removing previous artifact: {path}")
            shutil.rmtree(path)


def run_pyinstaller() -> Path:
    """Run PyInstaller using the repository spec file."""
    spec_file = REPO_ROOT / "installer" / "windows" / "clarity.spec"
    if not spec_file.exists():
        raise FileNotFoundError(f"Spec file not found at {spec_file}")

    print(f"[*] Building Clarity standalone CLI v{get_version()}...")
    print(f"[*] Repository root: {REPO_ROOT}")
    print(f"[*] Spec file: {spec_file}")

    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        str(spec_file),
    ]

    result = subprocess.run(cmd, cwd=str(REPO_ROOT), check=False)
    if result.returncode != 0:
        raise RuntimeError(f"PyInstaller build failed with exit code {result.returncode}")

    binary_name = "clarity.exe" if sys.platform == "win32" else "clarity"
    dist_binary = REPO_ROOT / "dist" / "clarity" / binary_name

    if not dist_binary.exists():
        raise FileNotFoundError(f"Expected compiled binary not found at {dist_binary}")

    # Ensure executable permissions on POSIX
    if sys.platform != "win32":
        dist_binary.chmod(0o755)

    print(f"[OK] Standalone binary successfully built at: {dist_binary}")
    return dist_binary


def main() -> int:
    parser = argparse.ArgumentParser(description="Build standalone Clarity CLI binary distribution.")
    parser.add_argument("--clean", action="store_true", help="Clean build directories before building.")
    args = parser.parse_args()

    try:
        if args.clean:
            clean_build_artifacts()
        binary_path = run_pyinstaller()
        print(f"\n[OK] Build complete: {binary_path}")
        return 0
    except Exception as exc:
        print(f"[!] Build error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
