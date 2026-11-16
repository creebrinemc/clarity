# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller specification file for the Clarity programming language standalone CLI."""

import os
import sys
from pathlib import Path

# Locate repository root relative to this spec file
spec_dir = Path(os.path.abspath(SPEC)).parent
repo_root = spec_dir.parent.parent

block_cipher = None

a = Analysis(
    [str(repo_root / "clarity" / "cli.py")],
    pathex=[str(repo_root)],
    binaries=[],
    datas=[],
    hiddenimports=[
        "clarity",
        "clarity.ast",
        "clarity.cli",
        "clarity.environment",
        "clarity.errors",
        "clarity.evaluator",
        "clarity.lexer",
        "clarity.modules",
        "clarity.parser",
        "clarity.project",
        "clarity.runtime",
        "clarity.semantics",
        "clarity.source",
        "clarity.stdlib",
        "clarity.tester",
        "clarity.tokens",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        "pytest",
        "unittest",
        "tkinter",
        "pydoc",
        "doctest",
        "difflib",
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher,
)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="clarity",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="clarity",
)
