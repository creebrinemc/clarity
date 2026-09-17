# The Clarity Ecosystem Architecture

Clarity is structured as a unified programming-language ecosystem composed of distinct, well-separated components. The core principle of this architecture is **strict decoupling**: the language implementation is independent of developer tooling, distribution mechanisms, web platforms, and editor integrations.

```
                         CLARITY ECOSYSTEM
                                 │
         ┌───────────────────────┼───────────────────────┐
         ▼                       ▼                       ▼
┌──────────────────┐   ┌───────────────────┐   ┌───────────────────┐
│     LANGUAGE     │   │     TOOLCHAIN     │   │      WEBSITE      │
│  (clarity core)  │   │  (tools, install) │   │ (clarity.creebrine)│
│                  │   │                   │   │                   │
│ • Lexer / Parser │   │ • CLI Runner      │   │ • Documentation   │
│ • AST & Spans    │   │ • Project Tools*  │   │ • Interactive Run*│
│ • Evaluator      │   │ • Test Harness*   │   │ • Downloads Hub*  │
│ • Runtime Values │   │ • Package Tool*   │   │ • Roadmap & News  │
│ • Standard Lib   │   │ • OS Installers*  │   └───────────────────┘
│ • SPEC.md        │   └─────────┬─────────┘
└────────┬─────────┘             │
         │                       │
         └───────────┬───────────┘
                     ▼
           ┌───────────────────┐
           │  CLARITY EDITOR*  │
           │ (dedicated IDE)   │
           │                   │
           │ • Syntax Colors   │
           │ • Diagnostics     │
           │ • Autocomplete    │
           │ • Run & Debug     │
           └───────────────────┘

  * Planned / Future milestone component
```

---

## Component Boundaries & Responsibilities

### 1. Clarity Language Core (`clarity/`)
The language core is the authoritative implementation of the Clarity language.

* **Responsibilities**:
  * Lexical analysis and source-span tokenization (`lexer.py`, `tokens.py`, `source.py`).
  * Syntax validation and AST construction (`parser.py`, `ast.py`).
  * Runtime environment, scope chains, and first-class functions (`runtime.py`, `environment.py`).
  * Language semantics and type rules (`semantics.py`).
  * Built-in standard library with swappable filesystem/random providers (`stdlib.py`).
  * Clear diagnostic errors with source coordinates (`errors.py`).
  * Authoritative language specification (`SPEC.md`).
* **Design Rule**: The language core must remain free of UI, GUI, or platform-specific installer dependencies. It operates entirely as an embeddable, headless interpreter.

### 2. Clarity Toolchain (`tools/`, `installer/`, `clarity/cli.py`)
The toolchain provides the developer interface for building, running, testing, and distributing Clarity software.

* **Components**:
  * **CLI (`clarity.cli`)**: Current command-line entrypoint to execute `.clr` source files and report versions.
  * **Project & Scaffolding Tooling (`tools/`)**: Future capabilities for creating new projects, scaffolding templates, running test suites, and formatting code.
  * **Native Installers (`installer/`)**: Future self-contained setup programs (Windows `.exe`, macOS `.pkg`/Homebrew, Linux packages) that bundle the standalone runtime, configure system `PATH`, and register `.clr` file associations.
* **Design Rule**: Toolchain components interface with the language core via clean programmatic APIs or CLI boundaries.

### 3. Clarity Website (`website/`)
The official public home of Clarity (`https://clarity.creebrine.com`).

* **Purpose**: *"Clarity — Code that speaks for itself."*
* **Planned Sections**:
  * **Home**: Philosophy, high-level features, and interactive sample code.
  * **Getting Started**: Quick setup guides for Windows, macOS, and Linux.
  * **Documentation**: Language reference, standard-library documentation, and guides.
  * **Examples**: Curated real-world Clarity scripts.
  * **Downloads**: Releases, installer links, and changelogs.
  * **Roadmap**: Transparent view into language milestones and ecosystem progress.
* **Design Rule**: The website documentation sources from repository documentation (`docs/`, `SPEC.md`) to maintain a single source of truth.

### 4. Clarity Editor (`editor/`)
A dedicated development environment tailored specifically for Clarity.

* **Vision**: A lightweight, responsive editor optimized for writing `.clr` code.
* **Planned Capabilities**:
  * Syntax highlighting tailored to Clarity keywords and English-style phrases.
  * Real-time parse diagnostics and syntax error reporting.
  * Context-aware autocompletion for builtins and user variables.
  * One-click execution and integrated output panel.
  * Future visual debugging and step-execution.
* **Design Rule**: The editor will consume language diagnostics and AST metadata through standardized language tools rather than reimplementing parser logic.

---

## Architectural Principles

1. **Zero Premature Complexity**: We design component boundaries early, but implement each component only when its time comes.
2. **Language Stability First**: The language engine remains pure, reliable, and regression-free as the ecosystem expands around it.
3. **Unified Identity**: Clarity is presented as a cohesive platform where language, tools, web presence, and editor speak a single design language.
