"""Entrypoint for executing Clarity package as a module (`python -m clarity`)."""

from clarity.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
