# Changelog

All notable changes to the Clarity programming language are documented in this file.

## [0.6.0] — Pending Release

### Added
- **Module & Import System (`clarity/modules.py`)**:
  - Whole-module imports (`import "path" as alias`) and named imports (`from "path" import name1, name2` or `name1 and name2`, with optional `as alias`).
  - Relative resolution (`./`, `../`), project-root resolution (`src/` then root), importing-file fallback, and `main.clr` / `mod.clr` directory entry resolution.
  - Singleton module caching by canonical path, isolated top-level module scopes, private `_`-prefixed identifiers, and circular dependency detection (`Clarity Circular Import Error`).
- **Dot Member Access (`clarity/tokens.py`, `clarity/parser.py`, `clarity/evaluator.py`)**:
  - Read-only `target.member` access for module exports and dictionary keys.
- **Static Project Manifest (`clarity/project.py`)**:
  - `conf.clr` parsed and statically validated at the AST level (`set project to { ... }`) without dynamic execution.
  - Upward project root discovery (`find_project_root`, `discover_project`) and Semantic Versioning validation.
- **Project & Test CLI (`clarity/cli.py`, `clarity/tester.py`, `clarity/__main__.py`)**:
  - `clarity run [entry]` — runs the project entry point or falls back to `src/main.clr` / `main.clr`.
  - `clarity new <name>` — scaffolds `conf.clr`, `README.md`, `src/main.clr`, and `tests/main_test.clr`.
  - `clarity test [path]` — discovers `*_test.clr` and `test_*.clr` files and executes top-level `test_*` functions.
  - `clarity help [command]` — prints top-level or command-specific help.
  - Preserved direct script execution (`clarity <file.clr>`) and `clarity --version` / `-v`.
- **Assertion Built-ins (`clarity/stdlib.py`)**:
  - `assert(condition [, message])` and `assert_equal(actual, expected [, message])`.
- **Standalone Packaging & Windows Installer (`installer/`, `.github/workflows/build-installer.yml`)**:
  - PyInstaller standalone CLI specification (`installer/windows/clarity.spec`) and build/verification scripts (`build_standalone.py`, `test_standalone.py`).
  - Inno Setup 6 Windows x64 installer (`installer/windows/clarity_setup.iss`, `generate_installer.py`) with `PATH` registration and `.clr` file associations.
  - GitHub Actions workflow (`build-installer.yml`) for cross-OS Python testing and Windows installer artifact builds.
- **Documentation & Tests**:
  - Added [docs/0.6-design.md](docs/0.6-design.md), [docs/releases/0.6.0.md](docs/releases/0.6.0.md), updated [SPEC.md](SPEC.md), [README.md](README.md), and guides.
  - Added 0.6.0 test suites (`test_frontend_0_6.py`, `test_modules_0_6.py`, `test_project_0_6.py`, `test_cli_and_tester_0_6.py`, `test_e2e_user_experience.py`), bringing total pytest coverage to 235 tests.

### Changed
- `import` and `as` are now reserved keywords in `clarity/lexer.py` (breaking change only for scripts using `import` or `as` as variable/function names).
- Added `ModuleError`, `CircularImportError`, and `ProjectError` diagnostic categories in `clarity/errors.py`.
- Updated `clarity/stdlib.py` `create_standard_library` to accept both `filesystem` and `fs` keyword arguments.
- Updated `website/` pages and documentation to reflect Clarity 0.6.0 and removed temporary `VisualQA` gallery assets.

## [0.5.0] — 2026-09-17

### Added
- Globally available standard library (`clarity/stdlib.py`): Text (`length`, `uppercase`, `lowercase`, `trim`, `contains`, `replace`, `split`, `join`), Collections (`reverse`, `sort`), Math (`abs`, `floor`, `ceil`, `round`, `min`, `max`, `sqrt`, `power`), Random (`random`, `choose`), and UTF-8 Filesystem (`read_file`, `write_file`, `file_exists`).
- Initial website portal (`website/`) and repository documentation (`SPEC.md`, `docs/`).

## [0.4.0] — 2026-09-17

### Added
- 0-based indexing and indexed assignments for lists and dictionaries, read-only string indexing, English comparison phrases (`is equal to`, `is at least`, etc.), `for each` loops, and `repeat N times` loops.

## [0.3.0] — 2026-09-17

### Added
- First-class functions (`function ... taking ... and ...`), `return` statements, recursion, and lexical closures.

## [0.2.0] — Earlier Prototype

### Added
- Control flow (`if` / `else if` / `else`, `while`, numeric range `for ... from ... to ... [step ...]`, `break`, and `continue`).

## [0.1.0] – [0.1.1] — Earlier Prototype

### Added
- Core lexer, recursive-descent parser, AST with source spans, evaluator, variable assignments (`set ... to ...`), arithmetic precedence, `say` output, `#` comments, and unary operators.
