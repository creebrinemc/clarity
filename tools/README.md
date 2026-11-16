# Clarity Toolchain (`tools/`)

This directory is reserved for developer toolchain components, CLI extensions, and project automation utilities for the Clarity ecosystem.

---

## Purpose & Planned Scope

The Clarity toolchain builds around the core language interpreter to provide high-level developer workflows:

1. **Project Scaffolding (`clarity new`)** *(available since 0.6.0)*: Initializing new Clarity projects with sensible directory structures and manifests.
2. **Test Runner (`clarity test`)** *(available since 0.6.0)*: Discovering and running Clarity-native test suites.
3. **Formatter (`clarity fmt`)**: Canonical source code formatting for `.clr` files.
4. **Package Tooling (Future)**: Dependency management and module resolution.

---

## Current Status

* The CLI is implemented at [`clarity/cli.py`](../clarity/cli.py). As of 0.6.0 it provides `clarity <file.clr>`, `clarity run`, `clarity new`, `clarity test`, `clarity help`, and `clarity --version`.
* Project configuration lives in [`clarity/project.py`](../clarity/project.py), and the test runner in [`clarity/tester.py`](../clarity/tester.py).
* The formatter and package tooling are planned for a future milestone.
