# Clarity Native Installer Architecture (`installer/`)

This directory contains the architecture, configuration scripts, and build tooling for distributing the Clarity programming language as a native, standalone application without requiring end users to manually install Python, configure virtual environments, or understand internal package structures.

---

## 1. Distribution Philosophy

Clarity is designed to feel like a real programming language from the moment of download:

```
Download Clarity Setup → Install → Open any terminal → clarity --version → Start coding!
```

### Core Requirements
1. **Zero Python Dependency**: The distributed package bundles a standalone runtime.
2. **Instant Execution**: Fast cold-start CLI performance without decompression lag.
3. **Seamless System Integration**: Automatic `PATH` configuration and `.clr` file association.
4. **Idempotent Upgrades & Clean Removal**: In-place version upgrades (0.6.0 is the first release with an installer) and complete uninstallation.

---

## 2. Packaging Decision Matrix

| Packaging Strategy | Cold-Start Latency | Package Size | Reliability & Maintenance | Antivirus Profile | Decision |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **PyInstaller (`--onedir`)** | **~25–45ms** (Fast) | ~35–45 MB | **High** (Standard, reproducible) | **Good** (Standard binary layout) | **Selected for Windows Installer** |
| **PyInstaller (`--onefile`)** | ~250–500ms (Decompress to `%TEMP%`) | ~18–25 MB | High | Medium (Temporary file extraction triggers heuristics) | Secondary (Portable single binary) |
| **Nuitka (C-Transpiler)** | ~20–35ms | ~30–40 MB | Medium (Requires MSVC/MinGW toolchain) | Good | Evaluated for future compiler milestone |
| **Embedded Python Shim** | ~40–60ms | ~25–35 MB | Medium (Custom launcher stub needed) | Good | Alternative portable option |

### Rationale
* **`--onedir` mode** is placed inside `C:\Program Files\Clarity` by the installer. Because the files are already unpacked on disk, invoking `clarity` has **zero decompression delay**, providing snappy terminal responsiveness.
* Combined with **Inno Setup 6**, the installer produces a single compressed `Clarity-<version>-Windows-x64-Setup.exe` (for this release, `Clarity-0.6.0-Windows-x64-Setup.exe`) that extracts the directory, configures PATH, registers file associations, and creates an official Windows Uninstaller.

---

## 3. Directory Layout

```
installer/
├── README.md                           # Architectural guide & build documentation
├── scripts/
│   ├── build_standalone.py             # Compiles standalone clarity CLI bundle via PyInstaller
│   ├── generate_installer.py           # Validates versions and invokes Inno Setup compiler
│   └── test_standalone.py              # Automated test suite for packaged binary artifacts
└── windows/
    ├── clarity.spec                    # PyInstaller build specification
    └── clarity_setup.iss               # Inno Setup 6 installer script
```

---

## 4. Build Process

### Prerequisites (For Developers Building Locally)
* **Python**: Version 3.11 or newer.
* **PyInstaller**: `pip install pyinstaller`.
* **Inno Setup 6** (Windows only): Download from [jrsoftware.org](https://jrsoftware.org/isdl.php).

### Step 1: Build the Standalone Binary
From the repository root:

```bash
python installer/scripts/build_standalone.py --clean
```

This generates `dist/clarity/` containing:
* `clarity.exe` (Windows) or `clarity` (macOS/Linux)
* Bundled Python runtime and compiled CPython extensions
* Base library archive

### Step 2: Validate the Standalone Binary
Run the automated test suite against the compiled binary:

```bash
python installer/scripts/test_standalone.py
```

Tests executed:
1. `clarity --version` &rarr; Verifies exact version string (`Clarity <version>`, read from `clarity/__init__.py`).
2. `clarity examples/hello.clr` &rarr; Verifies standard script execution.
3. `clarity examples/standard_library.clr` &rarr; Verifies built-in text/math/collections standard library.
4. Missing arguments &rarr; Verifies exit code 2 and usage message.
5. Syntax error handling &rarr; Verifies exit code 1 and structured diagnostic error output.
6. Nonexistent file error &rarr; Verifies exit code 1 and formatted file read error.
7. Standard library runtime error &rarr; Verifies exit code 1 and runtime error output.
8. Isolated environment & arbitrary directory execution &rarr; Verifies standalone operation without host virtual environment.

### Step 3: Compile the Windows Installer
On Windows (or in CI):

```bash
python installer/scripts/generate_installer.py --compile
```

Output artifact:
```
dist/installer/Clarity-0.6.0-Windows-x64-Setup.exe
```

---

## 5. Windows Installer Behavior & Specifications

### Installation Directory
* **Administrative Mode**: `C:\Program Files\Clarity`
* **Non-Administrative (Standard User)**: `%LOCALAPPDATA%\Programs\Clarity`

### PATH Environment Variable Integration
* The installer automatically registers `{app}` into the user or system `PATH` registry key (`Environment` or `System\CurrentControlSet\Control\Session Manager\Environment`) using `REG_EXPAND_SZ` to preserve expandable paths.
* The installer broadcasts `WM_SETTINGCHANGE` to top-level Windows handles so newly spawned command prompts (Command Prompt, Windows Terminal, PowerShell) immediately recognize `clarity` without a computer restart.
* On uninstallation, the directory is cleanly removed from the `PATH` string without truncating other entries.

### File Association (`.clr`)
* Registers `.clr` extension with ProgID `ClaritySourceFile`.
* **Double-Click Action (`open`)**: Executes the program in a console window with `pause` so that the output remains visible on screen rather than instantly closing.
* **Context Menu Actions**:
  * `"Run (Direct CLI)"`: Executes directly via `"{app}\clarity.exe" "%1"`.
  * `"Edit in Notepad"`: Opens the source file in Notepad (`"notepad.exe" "%1"`).
* Assigns `"{app}\clarity.exe,0"` as the default file icon.

### Safe In-Place Upgrades
* The installer uses a fixed `AppId`, so a future installer run over an existing 0.6.0 installation replaces the runtime files in-place and preserves PATH and file associations without creating duplicate entries. 0.6.0 is the first release with a Windows installer, so in-place upgrades will be verified against the next release.

---

## 6. Automated CI/CD Distribution

GitHub Actions workflow [`.github/workflows/build-installer.yml`](../.github/workflows/build-installer.yml) automatically:
1. Runs the full `pytest` regression suite (235 tests in 0.6.0) on Ubuntu, macOS, and Windows with Python 3.11 and 3.12.
2. Builds the standalone `clarity.exe` executable on a `windows-latest` runner.
3. Runs `test_standalone.py` to verify binary behavior.
4. Compiles `Clarity-0.6.0-Windows-x64-Setup.exe` with Inno Setup.
5. Uploads the installer and the portable `dist/clarity/` directory as workflow artifacts (retained for 14 days).

The workflow does not publish GitHub Releases. Release assets are attached manually after the CI artifacts are verified.

---

## 7. Multi-Platform Roadmap

* **macOS (Planned)**:
  * Signed `.pkg` installer deploying to `/usr/local/bin/clarity` or `/opt/clarity`.
  * Official Homebrew tap formula: `brew install clarity-lang/tap/clarity`.
* **Linux (Planned)**:
  * Native `.deb` (Debian/Ubuntu) and `.rpm` (Fedora/RHEL) packages.
  * Portable `.tar.gz` archive with a one-line install script (`curl -fsSL https://clarity.creebrine.com/install.sh | sh`).
