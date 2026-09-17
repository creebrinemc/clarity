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
│ • AST & Spans   │      │ • Project CLI*  │      │ • Examples Hub  │
│ • Runtime Engine│      │ • Test Runner*  │      │ • Downloads*    │
│ • Standard Lib  │      │ • OS Installer* │      │ • Roadmap       │
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
The pure, headless interpreter containing the lexer, parser, AST, runtime evaluator, first-class closures, and the built-in standard library.

### 2. [Toolchain](tools/) *(In Progress / Planned)*
Developer workflow tools including the current command-line runner, future project scaffolding (`clarity new`), test harness (`clarity test`), code formatter (`clarity fmt`), and [native OS installers](installer/).

### 3. [Website](website/) *(Planned)*
The official web platform at [**clarity.creebrine.com**](https://clarity.creebrine.com), serving as the central hub for interactive documentation, downloads, and community updates.

### 4. [Editor](editor/) *(Planned)*
A dedicated, lightweight development environment and IDE tailored specifically for `.clr` projects, featuring real-time diagnostics, syntax highlighting, and integrated execution.

For detailed architectural boundaries, see [docs/ecosystem.md](docs/ecosystem.md).

---

## Project Status & Roadmap

* **Current Version**: `0.5.0`
* **Status**: Early development

### Completed Milestones

* [x] **0.1.0 — Core**: Variables, arithmetic operators, precedence, `say` output, and diagnostic source spans.
* [x] **0.1.1 — Foundation Hardening**: Lexer improvements, comment support, unary operators, and error formatting.
* [x] **0.2.0 — Control Flow**: `if`/`else if`/`else`, `while` loops, numeric range loops, and `break`/`continue`.
* [x] **0.3.0 — Functions & Closures**: First-class functions, parameter chains (`taking ... and ...`), return statements, recursion, and lexical closures.
* [x] **0.4.0 — Data & Readability**: List/dict/string 0-based indexing, indexed assignments, English comparison phrases (`is at least`, `is greater than`), `for each` loops, and `repeat N times`.
* [x] **0.5.0 — Standard Library**: Built-in functions for Text, Collections, Math, Random selection, and Filesystem operations with zero Python exception leaks.

### Planned Direction

* [ ] **0.6.x — Modules & Project System**: File imports, namespaces, and multi-file projects.
* [ ] **Toolchain Enhancements**: Project generator, test runner, and canonical formatting CLI.
* [ ] **Native Installers**: Zero-config standalone installers for Windows (`.exe`), macOS, and Linux.
* [ ] **Website Launch**: Live documentation portal at [clarity.creebrine.com](https://clarity.creebrine.com).
* [ ] **Clarity Editor**: Dedicated development environment for `.clr` files.

---

## Quickstart

### Installation (Development Prototype)

Clarity requires Python 3.11+.

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
# Output: Clarity 0.5.0
```

### Running Programs

Run any `.clr` source file:

```bash
clarity examples/hello.clr
clarity examples/standard_library.clr
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

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
