"""Command-line entry point and project tooling for Clarity."""

import argparse
import sys
from pathlib import Path

try:
    from . import __version__
    from .errors import ClarityError, ProjectError
    from .evaluator import Evaluator
    from .lexer import Lexer
    from .modules import ModuleManager
    from .parser import Parser
    from .project import PROJECT_NAME_REGEX, discover_project, find_project_root
    from .tester import run_tests
except (ImportError, ValueError):
    from clarity import __version__
    from clarity.errors import ClarityError, ProjectError
    from clarity.evaluator import Evaluator
    from clarity.lexer import Lexer
    from clarity.modules import ModuleManager
    from clarity.parser import Parser
    from clarity.project import PROJECT_NAME_REGEX, discover_project, find_project_root
    from clarity.tester import run_tests


def run_source(source: str, current_file: Path | None = None, project_root: Path | None = None) -> object:
    manager = ModuleManager(project_root=project_root)
    evaluator = Evaluator(
        module_manager=manager,
        current_file=current_file,
        project_root=project_root,
    )
    tokens = Lexer(source).tokenize()
    tree = Parser(tokens).parse()
    return evaluator.evaluate(tree)


def run_file(file_path: Path, project_root: Path | None = None) -> int:
    resolved = file_path.resolve()
    if not resolved.is_file():
        print(f"Clarity Error\n\nCould not read {file_path}: No such file or directory")
        return 1
    try:
        source = resolved.read_text(encoding="utf-8")
    except OSError as error:
        print(f"Clarity Error\n\nCould not read {file_path}: {error}")
        return 1

    if project_root is None:
        project_root = find_project_root(resolved.parent)

    try:
        run_source(source, current_file=resolved, project_root=project_root)
    except ClarityError as error:
        print(error)
        return 1
    return 0


def cmd_run(args: argparse.Namespace) -> int:
    if args.entry:
        entry_path = Path(args.entry).resolve()
        if not entry_path.is_file():
            print(f"Clarity Error\n\nSpecified entry file not found: {args.entry}")
            return 1
        project_root = find_project_root(entry_path.parent)
        return run_file(entry_path, project_root=project_root)

    config = discover_project()
    if config is not None:
        entry_path = config.resolve_entry_path()
        if not entry_path.is_file():
            print(
                f"Clarity Project Error\n\n"
                f"Configured entry point not found: {config.entry}\n"
                f"Project root: {config.root}"
            )
            return 2
        return run_file(entry_path, project_root=config.root)

    # Zero-config fallback
    cwd = Path.cwd()
    if (cwd / "src" / "main.clr").is_file():
        return run_file(cwd / "src" / "main.clr", project_root=None)
    if (cwd / "main.clr").is_file():
        return run_file(cwd / "main.clr", project_root=None)

    print(
        "Clarity Project Error\n\n"
        "No Clarity project found (conf.clr not found in current or parent directories).\n"
        "To run a standalone script, use: clarity <file.clr>\n"
        "To initialize a new project, use: clarity new <project-name>"
    )
    return 2


def cmd_new(args: argparse.Namespace) -> int:
    name = args.name.strip()
    if not name or not PROJECT_NAME_REGEX.match(name):
        print(
            f"Clarity Project Error\n\n"
            f"Invalid project name '{name}'. Name must contain only alphanumeric characters, underscores, and hyphens."
        )
        return 2

    target_dir = Path.cwd() / name
    if target_dir.exists() and any(target_dir.iterdir()):
        print(f"Clarity Project Error\n\nDirectory '{name}' already exists and is not empty.")
        return 1

    try:
        src_dir = target_dir / "src"
        tests_dir = target_dir / "tests"
        src_dir.mkdir(parents=True, exist_ok=True)
        tests_dir.mkdir(parents=True, exist_ok=True)

        conf_content = (
            "# Clarity Project Configuration\n"
            "set project to {\n"
            f'    name: "{name}",\n'
            '    version: "0.1.0",\n'
            '    entry: "src/main.clr",\n'
            f'    description: "A Clarity project",\n'
            '    author: "",\n'
            '    license: "MIT"\n'
            "}\n"
        )
        (target_dir / "conf.clr").write_text(conf_content, encoding="utf-8")

        main_content = (
            "function greet taking name {\n"
            '    return "Hello, " + name + "!"\n'
            "}\n\n"
            'say greet("Clarity")\n'
        )
        (src_dir / "main.clr").write_text(main_content, encoding="utf-8")

        test_content = (
            'from "../src/main" import greet\n\n'
            "function test_greeting {\n"
            '    assert_equal(greet("World"), "Hello, World!", "Greeting should match expected output")\n'
            "}\n"
        )
        (tests_dir / "main_test.clr").write_text(test_content, encoding="utf-8")

        readme_content = (
            f"# {name}\n\n"
            "A Clarity 0.6 project.\n\n"
            "## Running\n\n"
            "```bash\n"
            "clarity run\n"
            "```\n\n"
            "## Testing\n\n"
            "```bash\n"
            "clarity test\n"
            "```\n"
        )
        (target_dir / "README.md").write_text(readme_content, encoding="utf-8")
    except OSError as err:
        print(f"Clarity Project Error\n\nCould not create project files: {err}")
        return 1

    print(f"[✓] Created Clarity project '{name}'")
    print(f"\nNext steps:\n  cd {name}\n  clarity run\n  clarity test\n")
    return 0


def cmd_test(args: argparse.Namespace) -> int:
    target_path = Path(args.path) if args.path else None
    try:
        summary = run_tests(target_path=target_path)
        return 0 if summary.is_success else 1
    except ClarityError as err:
        print(err)
        return 1
    except Exception as err:
        print(f"Clarity Test Error\n\n{err}")
        return 1


def main(argv: list[str] | None = None) -> int:
    args_list = sys.argv[1:] if argv is None else argv

    # Direct script execution check (backward compatibility)
    if args_list and not args_list[0].startswith("-"):
        first = args_list[0]
        if first not in {"run", "new", "test", "help"}:
            # Check if it's a file or ends in .clr
            file_candidate = Path(first)
            if file_candidate.is_file() or first.endswith(".clr"):
                return run_file(file_candidate)

    parser = argparse.ArgumentParser(
        prog="clarity",
        description="The Clarity programming language runtime and toolchain.",
    )
    parser.add_argument(
        "--version",
        "-v",
        action="version",
        version=f"Clarity {__version__}",
    )

    subparsers = parser.add_subparsers(dest="command", metavar="<command>")

    # clarity run [entry]
    run_parser = subparsers.add_parser("run", help="Run the current project or specified entry file.")
    run_parser.add_argument("entry", nargs="?", help="Optional entry file to execute (e.g. src/main.clr)")

    # clarity new <name>
    new_parser = subparsers.add_parser("new", help="Scaffold a new Clarity project.")
    new_parser.add_argument("name", help="Name of the new project directory")

    # clarity test [path]
    test_parser = subparsers.add_parser("test", help="Discover and execute project test suites.")
    test_parser.add_argument("path", nargs="?", help="Optional test directory or file path to run")

    # clarity help [cmd]
    help_parser = subparsers.add_parser("help", help="Display help for a command.")
    help_parser.add_argument("subcommand", nargs="?", help="Command to get help on")

    # Fallback file argument for top-level
    parser.add_argument("file", nargs="?", type=Path, help="A .clr source file to run directly (script mode)")

    parsed = parser.parse_args(args_list)

    if parsed.command == "run":
        return cmd_run(parsed)
    if parsed.command == "new":
        return cmd_new(parsed)
    if parsed.command == "test":
        return cmd_test(parsed)
    if parsed.command == "help":
        if parsed.subcommand == "run":
            run_parser.print_help()
        elif parsed.subcommand == "new":
            new_parser.print_help()
        elif parsed.subcommand == "test":
            test_parser.print_help()
        else:
            parser.print_help()
        return 0

    if parsed.file is not None:
        return run_file(parsed.file)

    parser.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
