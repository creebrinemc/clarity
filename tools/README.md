# Clarity Toolchain (`tools/`)

This directory is reserved for developer toolchain components, CLI extensions, and project automation utilities for the Clarity ecosystem.

---

## Purpose & Planned Scope

The Clarity toolchain builds around the core language interpreter to provide high-level developer workflows:

1. **Project Scaffolding (`clarity new`)**: Initializing new Clarity projects with sensible directory structures and manifests.
2. **Test Runner (`clarity test`)**: Discovering and running Clarity-native test suites.
3. **Formatter (`clarity fmt`)**: Canonical source code formatting for `.clr` files.
4. **Package Tooling (Future)**: Dependency management and module resolution.

---

## Current Status

* The current CLI entry point is implemented at [`clarity/cli.py`](../clarity/cli.py) and executes `.clr` scripts via `clarity <file.clr>`.
* Advanced project and toolchain commands will be introduced in future milestones.
