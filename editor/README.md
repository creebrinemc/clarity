# Clarity Editor (`editor/`)

This directory is reserved for the dedicated development environment and IDE integrations for the Clarity programming language.

---

## Vision & Planned Scope

The Clarity Editor is envisioned as a lightweight, focused editor tailored specifically for `.clr` development:

* **Syntax Highlighting**: Custom colorization for Clarity keywords, English comparison phrases, literals, and standard-library functions.
* **Diagnostics**: Real-time syntax validation, source-span error highlighting, and inline diagnostic messages.
* **Autocomplete**: Intelligent completion for variables, function names, and built-in standard library utilities.
* **One-Click Run**: Instant script execution with an integrated output console.
* **Project Management**: Multi-file project navigation, file tree, and workspace settings.
* **Formatting & Tools**: Integrated code formatter and test runner interfaces.

---

## Current Status

* The dedicated editor is planned for a future tooling milestone.
* The editor will communicate with the language engine via standard headless interfaces without coupling GUI code to the core interpreter.
