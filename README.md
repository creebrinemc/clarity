# Clarity

Clarity is an early, readable general-purpose programming language prototype. This repository contains Clarity 0.4.0: a hand-written lexer, recursive-descent parser, AST, and interpreter written in Python.

## Run an example

```bash
python -m clarity.cli examples/hello.clr
python -m clarity.cli examples/calculator.clr
python -m clarity.cli examples/control_flow.clr
python -m clarity.cli examples/functions.clr
python -m clarity.cli examples/data_access.clr
```

```clr
set user to {
    name: "Creebrine",
    scores: [95, 100]
}

if user["scores"][0] is at least 90 {
    say user["name"] + " passed with distinction!"
}

repeat 2 times {
    say "Keep up the great work!"
}
```

## Development

```bash
python -m pip install -e ".[dev]"
python -m pytest
```

Implemented syntax and limitations are recorded in [SPEC.md](SPEC.md).
