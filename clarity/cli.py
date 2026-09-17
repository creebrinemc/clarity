"""Command-line entry point for the Clarity interpreter."""

import argparse
from pathlib import Path

from . import __version__
from .errors import ClarityError
from .evaluator import Evaluator
from .lexer import Lexer
from .parser import Parser


def run_source(source: str) -> object:
    return Evaluator().evaluate(Parser(Lexer(source).tokenize()).parse())


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="clarity", description="Run Clarity source files.")
    parser.add_argument("file", nargs="?", type=Path, help="A .clr source file")
    parser.add_argument("--version", action="version", version=f"Clarity {__version__}")
    args = parser.parse_args(argv)
    if args.file is None:
        parser.print_help()
        return 2
    try:
        run_source(args.file.read_text(encoding="utf-8"))
    except OSError as error:
        print(f"Clarity Error\n\nCould not read {args.file}: {error}")
        return 1
    except ClarityError as error:
        print(error)
        return 1
    return 0


if __name__ == "__main__": raise SystemExit(main())
