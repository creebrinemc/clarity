#!/usr/bin/env python3
"""Automated test suite for verifying the packaged standalone Clarity CLI binary.

Usage:
    python installer/scripts/test_standalone.py [--binary /path/to/clarity]
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import clarity


def find_default_binary() -> Path:
    """Locate the built binary in dist/clarity/."""
    binary_name = "clarity.exe" if sys.platform == "win32" else "clarity"
    candidate = REPO_ROOT / "dist" / "clarity" / binary_name
    if not candidate.exists():
        raise FileNotFoundError(
            f"Compiled binary not found at {candidate}. Run build_standalone.py first."
        )
    return candidate


def run_binary_test(binary_path: Path) -> None:
    """Execute validation test cases against the compiled binary."""
    print(f"[*] Running standalone verification on: {binary_path}")
    expected_version = f"Clarity {clarity.__version__}"

    # Test 1: --version
    print("  [1/8] Testing --version flag...")
    res = subprocess.run([str(binary_path), "--version"], capture_output=True, text=True)
    if res.returncode != 0:
        raise AssertionError(f"--version returned non-zero code {res.returncode}: {res.stderr}")
    version_output = (res.stdout or res.stderr).strip()
    if expected_version not in version_output:
        raise AssertionError(f"Expected '{expected_version}' in output, got: '{version_output}'")
    print(f"        ✓ Version matched: {version_output}")

    # Test 2: Execute examples/hello.clr
    hello_file = REPO_ROOT / "examples" / "hello.clr"
    if hello_file.exists():
        print("  [2/8] Testing execution of hello.clr...")
        res = subprocess.run([str(binary_path), str(hello_file)], capture_output=True, text=True)
        if res.returncode != 0:
            raise AssertionError(f"hello.clr execution failed with code {res.returncode}: {res.stderr}")
        if "Hello, Clarity!" not in res.stdout:
            raise AssertionError(f"Expected 'Hello, Clarity!' in stdout, got: '{res.stdout}'")
        print("        ✓ hello.clr executed successfully")

    # Test 3: Execute standard library script
    stdlib_file = REPO_ROOT / "examples" / "standard_library.clr"
    if stdlib_file.exists():
        print("  [3/8] Testing standard library script...")
        res = subprocess.run([str(binary_path), str(stdlib_file)], capture_output=True, text=True)
        if res.returncode != 0:
            raise AssertionError(f"standard_library.clr execution failed: {res.stderr}")
        if "WELCOME TO CLARITY" not in res.stdout:
            raise AssertionError(f"Expected standard library output missing in: '{res.stdout}'")
        print("        ✓ standard_library.clr executed successfully")

    # Test 4: Missing argument / help output
    print("  [4/8] Testing no-argument usage help...")
    res = subprocess.run([str(binary_path)], capture_output=True, text=True)
    if res.returncode != 2:
        raise AssertionError(f"Expected exit code 2 on missing args, got {res.returncode}")
    print("        ✓ Correct exit code 2 and help printed")

    # Test 5: Error handling on syntax errors
    print("  [5/8] Testing error output on invalid Clarity syntax...")
    with tempfile.NamedTemporaryFile(mode="w", suffix=".clr", delete=False) as tf:
        tf.write('set = "invalid syntax"')
        temp_file_path = Path(tf.name)

    try:
        res = subprocess.run([str(binary_path), str(temp_file_path)], capture_output=True, text=True)
        if res.returncode != 1:
            raise AssertionError(f"Expected exit code 1 on error, got {res.returncode}")
        output = res.stdout + res.stderr
        if "Clarity " not in output or "Error" not in output:
            raise AssertionError(f"Expected formatted Clarity diagnostic error, got: '{output}'")
        print("        ✓ Clarity diagnostic error handled cleanly with exit code 1")
    finally:
        if temp_file_path.exists():
            temp_file_path.unlink()

    # Test 6: Nonexistent source file error
    print("  [6/8] Testing nonexistent source file handling...")
    nonexistent = Path(tempfile.gettempdir()) / "clarity_nonexistent_test_file.clr"
    res = subprocess.run([str(binary_path), str(nonexistent)], capture_output=True, text=True)
    if res.returncode != 1:
        raise AssertionError(f"Expected exit code 1 on nonexistent file, got {res.returncode}")
    if "Could not read" not in (res.stdout + res.stderr):
        raise AssertionError(f"Expected 'Could not read' error, got: '{res.stdout + res.stderr}'")
    print("        ✓ Nonexistent source file handled cleanly with exit code 1")

    # Test 7: Runtime error handling (Standard library runtime exception)
    print("  [7/8] Testing runtime error formatting from standard library...")
    with tempfile.NamedTemporaryFile(mode="w", suffix=".clr", delete=False) as tf:
        tf.write('read_file("nonexistent_clarity_test_file_9999.txt")')
        temp_runtime_file = Path(tf.name)

    try:
        res = subprocess.run([str(binary_path), str(temp_runtime_file)], capture_output=True, text=True)
        if res.returncode != 1:
            raise AssertionError(f"Expected exit code 1 on runtime error, got {res.returncode}")
        if "Clarity Runtime Error" not in (res.stdout + res.stderr):
            raise AssertionError(f"Expected 'Clarity Runtime Error', got: '{res.stdout + res.stderr}'")
        print("        ✓ Clarity Runtime Error handled cleanly with exit code 1")
    finally:
        if temp_runtime_file.exists():
            temp_runtime_file.unlink()

    # Test 8: Clean environment & arbitrary working directory execution
    print("  [8/8] Testing execution from arbitrary working directory with sanitized environment...")
    clean_env = {
        "PATH": os.environ.get("PATH", ""),
        "SYSTEMROOT": os.environ.get("SYSTEMROOT", ""),
        "TEMP": os.environ.get("TEMP", tempfile.gettempdir()),
        "TMP": os.environ.get("TMP", tempfile.gettempdir()),
        "USER": os.environ.get("USER", "test"),
        "HOME": os.environ.get("HOME", tempfile.gettempdir()),
    }
    with tempfile.TemporaryDirectory() as external_work_dir:
        test_script = Path(external_work_dir) / "test_prog.clr"
        test_script.write_text('say "Isolated execution: " + uppercase("ok")', encoding="utf-8")

        # Run with clean env and cwd set to external directory
        res = subprocess.run(
            [str(binary_path.resolve()), "test_prog.clr"],
            cwd=external_work_dir,
            env=clean_env,
            capture_output=True,
            text=True,
        )
        if res.returncode != 0:
            raise AssertionError(f"Isolated cwd execution failed: {res.stderr}")
        if "Isolated execution: OK" not in res.stdout:
            raise AssertionError(f"Expected 'Isolated execution: OK', got: '{res.stdout}'")
        print("        ✓ Arbitrary directory execution with sanitized environment passed")

    print(f"\n[✓] All 8 standalone binary verification tests passed for Clarity {clarity.__version__}!")


def main() -> int:
    parser = argparse.ArgumentParser(description="Test standalone Clarity binary artifact.")
    parser.add_argument("--binary", type=Path, help="Path to clarity executable (defaults to dist/clarity/clarity)")
    args = parser.parse_args()

    try:
        binary_path = args.binary or find_default_binary()
        run_binary_test(binary_path)
        return 0
    except Exception as exc:
        print(f"[!] Test failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
