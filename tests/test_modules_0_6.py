"""Tests for Clarity 0.6 module resolution, isolation, caching, and cycle detection."""

import pytest
from pathlib import Path
from clarity.lexer import Lexer
from clarity.parser import Parser
from clarity.evaluator import Evaluator
from clarity.modules import ModuleManager
from clarity.errors import ModuleError, CircularImportError, RuntimeError


def run_code(source: str, current_file: Path | None = None, project_root: Path | None = None, output_fn=None):
    output_lines = []
    out = output_fn or output_lines.append
    manager = ModuleManager(project_root=project_root, output=out)
    tokens = Lexer(source).tokenize()
    tree = Parser(tokens).parse()
    evaluator = Evaluator(
        module_manager=manager,
        current_file=current_file,
        project_root=project_root,
        output=out,
    )
    result = evaluator.evaluate(tree)
    return result, output_lines


def test_basic_relative_import(tmp_path: Path):
    utils_file = tmp_path / "utils.clr"
    utils_file.write_text(
        'function greet taking name {\n    return "Hello, " + name\n}\nset default_name to "World"\n',
        encoding="utf-8",
    )
    main_file = tmp_path / "main.clr"
    main_source = (
        'from "./utils" import greet, default_name\n'
        'say greet(default_name)\n'
    )
    _, output = run_code(main_source, current_file=main_file)
    assert output == ["Hello, World"]


def test_whole_module_import_and_dot_access(tmp_path: Path):
    math_file = tmp_path / "math_ops.clr"
    math_file.write_text(
        'function add taking a and b { return a + b }\n'
        'function multiply taking a and b { return a * b }\n',
        encoding="utf-8",
    )
    main_file = tmp_path / "main.clr"
    main_source = (
        'import "./math_ops" as math\n'
        'say math.add(10, 20)\n'
        'say math.multiply(4, 5)\n'
    )
    _, output = run_code(main_source, current_file=main_file)
    assert output == ["30", "20"]


def test_selective_import_with_and_and_aliases(tmp_path: Path):
    helpers_file = tmp_path / "helpers.clr"
    helpers_file.write_text(
        'function first { return 1 }\nfunction second { return 2 }\n',
        encoding="utf-8",
    )
    main_file = tmp_path / "main.clr"
    main_source = (
        'from "./helpers" import first as a and second as b\n'
        'say a() + b()\n'
    )
    _, output = run_code(main_source, current_file=main_file)
    assert output == ["3"]


def test_module_caching_and_singleton_execution(tmp_path: Path):
    counter_file = tmp_path / "counter.clr"
    counter_file.write_text(
        'say "Counter initialized"\n'
        'set count to 1\n'
        'function increment { set count to count + 1 }\n',
        encoding="utf-8",
    )
    main_file = tmp_path / "main.clr"
    main_source = (
        'import "./counter" as c1\n'
        'import "./counter" as c2\n'
        'say c1.count\n'
        'c1.increment()\n'
        'say c2.count\n'
    )
    _, output = run_code(main_source, current_file=main_file)
    # "Counter initialized" should only be printed ONCE
    assert output == ["Counter initialized", "1", "2"]


def test_module_isolation(tmp_path: Path):
    mod_file = tmp_path / "mod.clr"
    mod_file.write_text('set secret to "top-secret"\n', encoding="utf-8")
    main_file = tmp_path / "main.clr"
    main_source = (
        'import "./mod" as m\n'
        'say secret\n'  # secret not imported, should raise error
    )
    with pytest.raises(RuntimeError, match="Unknown variable: secret"):
        run_code(main_source, current_file=main_file)


def test_private_symbols_rejected(tmp_path: Path):
    lib_file = tmp_path / "lib.clr"
    lib_file.write_text(
        'function _internal { return "hidden" }\n'
        'function public_fn { return "visible" }\n',
        encoding="utf-8",
    )
    main_file = tmp_path / "main.clr"

    # 1. from import private
    with pytest.raises(RuntimeError, match="Cannot access private identifier '_internal'"):
        run_code('from "./lib" import _internal', current_file=main_file)

    # 2. dot access private
    with pytest.raises(RuntimeError, match="Cannot access private identifier '_internal'"):
        run_code('import "./lib" as l\nsay l._internal()', current_file=main_file)


def test_missing_module_error(tmp_path: Path):
    main_file = tmp_path / "main.clr"
    with pytest.raises(ModuleError, match='Could not find module "./nonexistent"'):
        run_code('from "./nonexistent" import foo', current_file=main_file)


def test_missing_export_error(tmp_path: Path):
    mod_file = tmp_path / "mod.clr"
    mod_file.write_text('set x to 10\n', encoding="utf-8")
    main_file = tmp_path / "main.clr"
    with pytest.raises(RuntimeError, match="Module 'mod' has no exported member 'missing'"):
        run_code('from "./mod" import missing', current_file=main_file)


def test_circular_import_detection(tmp_path: Path):
    a_file = tmp_path / "a.clr"
    b_file = tmp_path / "b.clr"
    a_file.write_text('import "./b" as b\nset val_a to 1\n', encoding="utf-8")
    b_file.write_text('import "./a" as a\nset val_b to 2\n', encoding="utf-8")

    with pytest.raises(CircularImportError, match="Detected circular dependency"):
        run_code('import "./a" as a', current_file=a_file)


def test_dictionary_dot_property_access():
    source = (
        'set user to { name: "Creebrine", age: 14 }\n'
        'say user.name\n'
        'say user.age\n'
    )
    _, output = run_code(source)
    assert output == ["Creebrine", "14"]


def test_dictionary_dot_property_missing():
    source = (
        'set user to { name: "Creebrine" }\n'
        'say user.missing\n'
    )
    with pytest.raises(RuntimeError, match="Property 'missing' not found in dictionary"):
        run_code(source)


def test_non_object_dot_property_error():
    source = (
        'set num to 42\n'
        'say num.foo\n'
    )
    with pytest.raises(RuntimeError, match="Cannot access property 'foo' on non-object type"):
        run_code(source)
