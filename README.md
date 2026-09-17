# Clarity

Clarity is an early, readable general-purpose programming language prototype. This repository contains Clarity 0.5.0: a hand-written lexer, recursive-descent parser, AST, interpreter, and built-in standard library written in Python.

## Run an example

```bash
python -m clarity.cli examples/hello.clr
python -m clarity.cli examples/calculator.clr
python -m clarity.cli examples/control_flow.clr
python -m clarity.cli examples/functions.clr
python -m clarity.cli examples/data_access.clr
python -m clarity.cli examples/standard_library.clr
```

```clr
set name to "  Clarity  "
say uppercase(trim(name))

set scores to [88, 42, 95, 70]
say "Sorted: " + sort(scores)
say "Lowest: " + min(scores)
say "Square root: " + sqrt(81)

set roll to random(1, 6)
say "Dice roll: " + roll
```

## Development

```bash
python -m pip install -e ".[dev]"
python -m pytest
```

Implemented syntax, standard-library documentation, and limitations are recorded in [SPEC.md](SPEC.md).
