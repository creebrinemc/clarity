# Clarity

**Code that speaks for itself.**

Clarity is a general-purpose programming language designed around readable, expressive syntax without sacrificing structural certainty or future power. It aims to read like structured English while remaining concise, predictable, and easy to learn.

Clarity source files use the `.clr` extension.

```clr
set user to {
    name: "Creebrine",
    score: 100
}

function greet taking person {
    say "Hello, " + person["name"] + "!"
}

if user["score"] is at least 100 {
    greet(user)
}
```

---

## The Clarity Ecosystem

Clarity is developed as a cohesive ecosystem designed with clean boundaries between its core language and developer tooling:

```
                      ┌────────────────────────┐
                      │    CLARITY ECOSYSTEM   │
                      └───────────┬────────────┘
         ┌────────────────────────┼────────────────────────┐
         ▼                        ▼                        ▼
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│    LANGUAGE     │      │    TOOLCHAIN    │      │     WEBSITE     │
│  (clarity core) │      │ (tools/install) │      │(clarity.creebrine)│
│                 │      │                 │      │                 │
│ • Lexer/Parser  │      │ • CLI Runner    │      │ • Docs & Guides │
│ • AST & Spans   │      │ • Project CLI   │      │ • Examples Hub  │
│ • Modules       │      │ • Test Runner   │      │ • Downloads*    │
│ • Runtime Engine│      │ • Win Installer │      │ • Roadmap       │
│ • Standard Lib  │      │ • macOS/Linux*  │      │                 │
└────────┬────────┘      └────────┬────────┘      └─────────────────┘
         │                        │
         └───────────┬────────────┘
                     ▼
           ┌───────────────────┐
           │  CLARITY EDITOR*  │
           │  (dedicated IDE)  │
           │                   │
           │ • Syntax Colors   │
           │ • Diagnostics     │
           │ • Autocomplete    │
           │ • Run & Debug     │
           └───────────────────┘

  * Planned component
```

### 1. [Language Core](clarity/)
The pure, headless interpreter containing the lexer, parser, AST, runtime evaluator, first-class closures, the module system, and the built-in standard library.

### 2. [Toolchain](tools/) *(In Progress)*
Developer workflow tools: the command-line runner (`clarity <file.clr>`, `clarity run`), project scaffolding (`clarity new`), the native test runner (`clarity test`), and the [Windows native installer](installer/). A formatter, linter, and macOS/Linux installers are planned.

### 3. [Website](website/) *(In Development)*
The official web platform at [**clarity.creebrine.com**](https://clarity.creebrine.com), serving as the central hub for interactive documentation, downloads, and community updates.

### 4. [Editor](editor/) *(Planned)*
A dedicated, lightweight development environment and IDE tailored specifically for `.clr` projects, featuring real-time diagnostics, syntax highlighting, and integrated execution.

For detailed architectural boundaries, see [docs/ecosystem.md](docs/ecosystem.md).

---

## Project Status & Roadmap

* **Current Version**: `0.6.0`
* **Status**: Early development
* **Changelog**: [CHANGELOG.md](CHANGELOG.md)

### Completed Milestones

* [x] **0.1.0 — Core**: Variables, arithmetic operators, precedence, `say` output, and diagnostic source spans.
* [x] **0.1.1 — Foundation Hardening**: Lexer improvements, comment support, unary operators, and error formatting.
* [x] **0.2.0 — Control Flow**: `if`/`else if`/`else`, `while` loops, numeric range loops, and `break`/`continue`.
* [x] **0.3.0 — Functions & Closures**: First-class functions, parameter chains (`taking ... and ...`), return statements, recursion, and lexical closures.
* [x] **0.4.0 — Data & Readability**: List/dict/string 0-based indexing, indexed assignments, English comparison phrases (`is at least`, `is greater than`), `for each` loops, and `repeat N times`.
* [x] **0.5.0 — Standard Library**: Built-in functions for Text, Collections, Math, Random selection, and Filesystem operations with zero Python exception leaks.
* [x] **0.6.0 — Modules & Projects**: `import`/`from ... import` with quoted paths, dot member access, `conf.clr` project manifests, `clarity run` / `clarity new` / `clarity test`, `assert` / `assert_equal`, standalone binary packaging, and the Windows installer.

### Planned Direction

* [ ] **0.7.0 — Development Ecosystem**: Formatter, linter, language server and editor integration, optional types, structured error handling, package management, and Clarity Learn.
* [ ] **Native Installers**: Homebrew (macOS), WinGet (Windows), and Linux packages.
* [ ] **Website Launch**: Live documentation portal at [clarity.creebrine.com](https://clarity.creebrine.com).
* [ ] **Clarity Editor**: Dedicated development environment for `.clr` files.

---

## Quickstart

### Windows Installer

Download `Clarity-0.6.0-Windows-x64-Setup.exe` from [GitHub Releases](https://github.com/creebrinemc/clarity/releases). It installs a standalone runtime (no Python required), optionally adds Clarity to `PATH`, and registers `.clr` file associations. See [installer/README.md](installer/README.md).

### Installation from Source (macOS, Linux, Windows)

Running from source requires Python 3.11+.

```bash
git clone https://github.com/creebrinemc/clarity.git
cd clarity

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install Clarity in editable mode
pip install -e ".[dev]"
```

Verify the installation:

```bash
clarity --version
# Output: Clarity 0.6.0
```

### Running Programs

Run any `.clr` source file:

```bash
clarity examples/hello.clr
clarity examples/standard_library.clr
```

### Creating a Project

```bash
clarity new my-app
cd my-app
clarity run    # runs the entry point declared in conf.clr
clarity test   # discovers and runs tests/*_test.clr
```

---

## Documentation

* [Getting Started Guide](docs/getting-started.md)
* [Language Guide](docs/language.md)
* [Standard Library Reference](docs/standard-library.md)
* [Examples Walkthrough](docs/examples.md)
* [Ecosystem Architecture](docs/ecosystem.md)
* [Language Specification (SPEC.md)](SPEC.md)

---

## Running Tests

Run the complete test suite with `pytest`:

```bash
python -m pytest -v
```

Packaging and installer checks are documented in [installer/README.md](installer/README.md).

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
