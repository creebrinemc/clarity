"""Project configuration loading, static AST validation, and project root discovery."""

import re
from dataclasses import dataclass, field
from pathlib import Path

from . import ast
from .errors import ProjectError
from .lexer import Lexer
from .parser import Parser

SEMVER_REGEX = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$")
PROJECT_NAME_REGEX = re.compile(r"^[a-zA-Z0-9_-]+$")


@dataclass(slots=True)
class ProjectConfig:
    name: str
    version: str
    entry: str
    root: Path
    description: str = ""
    author: str = ""
    license: str = ""
    dependencies: dict[str, str] = field(default_factory=dict)
    raw: dict[str, object] = field(default_factory=dict)

    def resolve_entry_path(self, explicit_entry: str | Path | None = None) -> Path:
        """Resolve the entry file to an absolute path."""
        if explicit_entry is not None:
            target = Path(explicit_entry)
            if target.is_absolute():
                return target
            return (self.root / target).resolve()
        return (self.root / self.entry).resolve()


def _extract_static_literal(node: ast.Node) -> object:
    """Extract Python literal value from AST node; reject all dynamic nodes."""
    if isinstance(node, ast.LiteralNode):
        return node.value
    if isinstance(node, ast.ListNode):
        return [_extract_static_literal(el) for el in node.elements]
    if isinstance(node, ast.DictionaryNode):
        result = {}
        for key_node, val_node in node.entries:
            key = _extract_static_literal(key_node)
            if not isinstance(key, (str, int, float, bool)):
                raise ProjectError(
                    f"Dictionary key in conf.clr must be a literal string or number, got {type(key).__name__}",
                    key_node.span,
                )
            result[str(key)] = _extract_static_literal(val_node)
        return result
    raise ProjectError(
        f"conf.clr must contain only static literal values (found dynamic {type(node).__name__})",
        getattr(node, "span", None),
    )


def load_project_config(conf_path: Path) -> ProjectConfig:
    """Parse and statically validate conf.clr without dynamic evaluation."""
    conf_file = conf_path.resolve()
    if not conf_file.is_file():
        raise ProjectError(f"Configuration file not found: {conf_file}")

    try:
        source = conf_file.read_text(encoding="utf-8")
    except OSError as err:
        raise ProjectError(f"Could not read conf.clr at {conf_file}: {err}")

    tokens = Lexer(source).tokenize()
    tree = Parser(tokens).parse()

    if not tree.statements:
        raise ProjectError("conf.clr cannot be empty; it must contain 'set project to { ... }'", tree.span)

    if len(tree.statements) != 1:
        raise ProjectError(
            "conf.clr must contain only a single top-level 'set project to { ... }' statement",
            tree.statements[1].span if len(tree.statements) > 1 else tree.span,
        )

    statement = tree.statements[0]
    if not isinstance(statement, ast.AssignNode) or statement.name != "project":
        raise ProjectError(
            "conf.clr must assign project metadata using 'set project to { ... }'",
            statement.span,
        )

    if not isinstance(statement.expression, ast.DictionaryNode):
        raise ProjectError(
            "The 'project' configuration must be a dictionary literal: 'set project to { ... }'",
            statement.expression.span,
        )

    raw_dict = _extract_static_literal(statement.expression)
    if not isinstance(raw_dict, dict):
        raise ProjectError("Invalid configuration dictionary in conf.clr", statement.expression.span)

    # Validate required fields
    if "name" not in raw_dict:
        raise ProjectError("Missing required field 'name' in conf.clr project dictionary", statement.span)
    name = raw_dict["name"]
    if not isinstance(name, str) or not name.strip():
        raise ProjectError("The 'name' field in conf.clr must be a non-empty string", statement.span)
    if not PROJECT_NAME_REGEX.match(name):
        raise ProjectError(
            f"Invalid project name '{name}' in conf.clr. Name must contain only alphanumeric characters, underscores, and hyphens.",
            statement.span,
        )

    if "version" not in raw_dict:
        raise ProjectError("Missing required field 'version' in conf.clr project dictionary", statement.span)
    version = raw_dict["version"]
    if not isinstance(version, str) or not version.strip():
        raise ProjectError("The 'version' field in conf.clr must be a non-empty string", statement.span)
    if not SEMVER_REGEX.match(version):
        raise ProjectError(
            f"Invalid version '{version}' in conf.clr. Version must follow Semantic Versioning (e.g. '0.1.0')",
            statement.span,
        )

    # Entry point determination
    project_root = conf_file.parent
    if "entry" in raw_dict:
        entry = raw_dict["entry"]
        if not isinstance(entry, str) or not entry.strip():
            raise ProjectError("The 'entry' field in conf.clr must be a valid path string", statement.span)
    else:
        # Default entry heuristic
        if (project_root / "src" / "main.clr").is_file():
            entry = "src/main.clr"
        elif (project_root / "main.clr").is_file():
            entry = "main.clr"
        elif (project_root / "src").is_dir():
            entry = "src/main.clr"
        else:
            entry = "main.clr"

    description = str(raw_dict.get("description", ""))
    author = str(raw_dict.get("author", ""))
    license_str = str(raw_dict.get("license", ""))
    dependencies = raw_dict.get("dependencies", {})
    if not isinstance(dependencies, dict):
        dependencies = {}

    return ProjectConfig(
        name=name,
        version=version,
        entry=entry,
        root=project_root,
        description=description,
        author=author,
        license=license_str,
        dependencies=dependencies,
        raw=raw_dict,
    )


def find_project_root(start_dir: Path | None = None) -> Path | None:
    """Traverse upward from start_dir to find the nearest directory containing conf.clr."""
    current = (start_dir or Path.cwd()).resolve()
    while True:
        if (current / "conf.clr").is_file():
            return current
        if current.parent == current:
            return None
        current = current.parent


def discover_project(start_dir: Path | None = None) -> ProjectConfig | None:
    """Discover and load the nearest project configuration."""
    root = find_project_root(start_dir)
    if root is None:
        return None
    return load_project_config(root / "conf.clr")
