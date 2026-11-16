"""End-to-end integration tests simulating real developer workflows in Clarity 0.6."""

import subprocess
import sys
from pathlib import Path
from clarity.cli import main


def test_full_project_lifecycle(tmp_path: Path, monkeypatch, capsys):
    # 1. Start in an empty workspace
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    monkeypatch.chdir(workspace)

    # 2. Run clarity new my-service
    code_new = main(["new", "my-service"])
    assert code_new == 0
    project_dir = workspace / "my-service"
    assert project_dir.is_dir()

    # 3. Add a helper module in src/math_utils.clr
    math_utils = project_dir / "src" / "math_utils.clr"
    math_utils.write_text(
        'function square taking n { return n * n }\n'
        'function cube taking n { return n * n * n }\n',
        encoding="utf-8",
    )

    # 4. Update src/main.clr to import math_utils and use dot access
    main_file = project_dir / "src" / "main.clr"
    main_file.write_text(
        'from "./math_utils" import square and cube\n\n'
        'function greet taking name {\n'
        '    return "Hello, " + name + "!"\n'
        '}\n\n'
        'set user to { name: "Alice", value: 5 }\n'
        'say "User: " + user.name\n'
        'say "Square: " + square(user.value)\n'
        'say "Cube: " + cube(user.value)\n',
        encoding="utf-8",
    )

    # 5. Add a test in tests/math_test.clr
    test_file = project_dir / "tests" / "math_test.clr"
    test_file.write_text(
        'from "../src/math_utils" import square and cube\n\n'
        'function test_square {\n'
        '    assert_equal(square(4), 16, "4 squared is 16")\n'
        '}\n\n'
        'function test_cube {\n'
        '    assert_equal(cube(3), 27, "3 cubed is 27")\n'
        '}\n',
        encoding="utf-8",
    )

    # 6. Run clarity run from project root
    monkeypatch.chdir(project_dir)
    code_run = main(["run"])
    assert code_run == 0
    captured = capsys.readouterr()
    assert "User: Alice" in captured.out
    assert "Square: 25" in captured.out
    assert "Cube: 125" in captured.out

    # 7. Run clarity test from project root
    code_test = main(["test"])
    assert code_test == 0
    captured_test = capsys.readouterr()
    assert "tests/main_test.clr > test_greeting" in captured_test.out
    assert "tests/math_test.clr > test_cube" in captured_test.out
    assert "tests/math_test.clr > test_square" in captured_test.out
    assert "Status: PASSED" in captured_test.out

    # 8. Test upward discovery from nested subdirectory (e.g. inside src/)
    monkeypatch.chdir(project_dir / "src")
    code_run_nested = main(["run"])
    assert code_run_nested == 0
    captured_nested = capsys.readouterr()
    assert "User: Alice" in captured_nested.out

    # 9. Test standalone script mode outside project
    standalone_file = workspace / "standalone.clr"
    standalone_file.write_text('say "Standalone 0.6 Script"', encoding="utf-8")
    monkeypatch.chdir(workspace)
    code_script = main([str(standalone_file)])
    assert code_script == 0
    captured_script = capsys.readouterr()
    assert "Standalone 0.6 Script" in captured_script.out
