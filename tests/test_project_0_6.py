"""Tests for Clarity 0.6 project configuration parsing and directory discovery."""

import pytest
from pathlib import Path
from clarity.project import (
    load_project_config,
    find_project_root,
    discover_project,
)
from clarity.errors import ProjectError


def test_valid_project_config(tmp_path: Path):
    conf_file = tmp_path / "conf.clr"
    conf_file.write_text(
        'set project to {\n'
        '    name: "my-app",\n'
        '    version: "0.1.0",\n'
        '    entry: "src/main.clr",\n'
        '    description: "A test project",\n'
        '    author: "Creebrine",\n'
        '    license: "MIT"\n'
        '}\n',
        encoding="utf-8",
    )
    config = load_project_config(conf_file)
    assert config.name == "my-app"
    assert config.version == "0.1.0"
    assert config.entry == "src/main.clr"
    assert config.description == "A test project"
    assert config.author == "Creebrine"
    assert config.license == "MIT"
    assert config.root == tmp_path


def test_default_entry_inference(tmp_path: Path):
    # Case 1: src/main.clr exists
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "main.clr").write_text('say "hi"', encoding="utf-8")
    conf_file = tmp_path / "conf.clr"
    conf_file.write_text('set project to { name: "demo", version: "1.0.0" }', encoding="utf-8")
    config = load_project_config(conf_file)
    assert config.entry == "src/main.clr"

    # Case 2: only main.clr exists
    tmp2 = tmp_path / "t2"
    tmp2.mkdir()
    (tmp2 / "main.clr").write_text('say "hi"', encoding="utf-8")
    conf2 = tmp2 / "conf.clr"
    conf2.write_text('set project to { name: "demo2", version: "1.0.0" }', encoding="utf-8")
    config2 = load_project_config(conf2)
    assert config2.entry == "main.clr"


def test_reject_dynamic_expressions_in_conf(tmp_path: Path):
    conf_file = tmp_path / "conf.clr"
    conf_file.write_text(
        'set project to {\n'
        '    name: "my-" + "app",\n'  # dynamic binary op!
        '    version: "0.1.0"\n'
        '}\n',
        encoding="utf-8",
    )
    with pytest.raises(ProjectError, match="conf.clr must contain only static literal values"):
        load_project_config(conf_file)


def test_reject_missing_required_fields(tmp_path: Path):
    # Missing name
    c1 = tmp_path / "c1.clr"
    c1.write_text('set project to { version: "0.1.0" }', encoding="utf-8")
    with pytest.raises(ProjectError, match="Missing required field 'name'"):
        load_project_config(c1)

    # Missing version
    c2 = tmp_path / "c2.clr"
    c2.write_text('set project to { name: "app" }', encoding="utf-8")
    with pytest.raises(ProjectError, match="Missing required field 'version'"):
        load_project_config(c2)


def test_reject_invalid_version_and_name(tmp_path: Path):
    c1 = tmp_path / "c1.clr"
    c1.write_text('set project to { name: "app", version: "not-a-version" }', encoding="utf-8")
    with pytest.raises(ProjectError, match="Invalid version 'not-a-version'"):
        load_project_config(c1)

    c2 = tmp_path / "c2.clr"
    c2.write_text('set project to { name: "my app with spaces", version: "1.0.0" }', encoding="utf-8")
    with pytest.raises(ProjectError, match="Invalid project name"):
        load_project_config(c2)


def test_project_discovery_upward_traversal(tmp_path: Path):
    project_root = tmp_path / "workspace" / "my-project"
    nested_dir = project_root / "src" / "utils" / "deep"
    nested_dir.mkdir(parents=True)

    conf_file = project_root / "conf.clr"
    conf_file.write_text('set project to { name: "deep-app", version: "0.1.0" }', encoding="utf-8")

    # Discover from deep directory
    found_root = find_project_root(nested_dir)
    assert found_root == project_root.resolve()

    config = discover_project(nested_dir)
    assert config is not None
    assert config.name == "deep-app"


def test_zero_config_discovery(tmp_path: Path):
    empty_dir = tmp_path / "empty"
    empty_dir.mkdir()
    assert find_project_root(empty_dir) is None
    assert discover_project(empty_dir) is None
