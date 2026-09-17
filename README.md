# Clarity

Clarity is an early, readable general-purpose programming language prototype. This repository contains Clarity 0.3.0: a hand-written lexer, recursive-descent parser, AST, and interpreter written in Python.

## Run an example

```bash
python -m clarity.cli examples/hello.clr
python -m clarity.cli examples/calculator.clr
python -m clarity.cli examples/control_flow.clr
python -m clarity.cli examples/functions.clr
```

```clr
function greet taking name {
    say "Hello, " + name
}

function add taking a and b {
    return a + b
}

greet("Creebrine")
set total to add(10, 20)
say "Total: " + total
```

## Development

```bash
python -m pip install -e ".[dev]"
python -m pytest
```

Implemented syntax and limitations are recorded in [SPEC.md](SPEC.md).
