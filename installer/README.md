# Clarity Native Installers (`installer/`)

This directory is reserved for native packaging and installer configurations for distributing Clarity across major operating systems.

---

## Planned Architecture & Distribution Strategy

The goal of Clarity installers is to provide a zero-configuration, native installation experience without requiring users to manually install Python or manage virtual environments.

### Target Experience (Windows)

```
Clarity Setup.exe
  ↓
Install Clarity
  ↓
Bundle standalone runtime
  ↓
Add Clarity to system PATH
  ↓
Associate .clr files
  ↓
Finish: Run `clarity script.clr` in any terminal
```

---

## Target Platforms

* **Windows**: Standalone installer (`.exe` / `.msi`) bundling the runtime and configuring PATH and `.clr` shell association.
* **macOS**: Signed `.pkg` installer and Homebrew formula (`brew install clarity`).
* **Linux**: Native packages (`.deb`, `.rpm`) and standalone install script.

---

## Current Status

* Native installers are planned for future distribution milestones.
* For current development installation instructions, see [docs/getting-started.md](../docs/getting-started.md).
