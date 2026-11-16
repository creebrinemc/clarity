"""Tests for Clarity 0.6 CLI subcommands (run, new, test) and the native test runner."""

import io
import pytest
from pathlib import Path
from clarity.cli import main
from clarity.tester import run_tests, discover_test_files, run_test_file
from clarity.stdlib import get_standard_library


def test_cli_version(capsys):
    with pytest.raises(SystemExit) as exc:
        main(["--version"])
    assert exc.value.code == 0
    captured = capsys.readouterr()
    assert "Clarity" in captured.out


def test_cli_script_mode(tmp_path: Path, capsys):
    script = tmp_path / "hello.clr"
    script.write_text('say "Script Mode Works!"', encoding="utf-8")

    code = main([str(script)])
    assert code == 0
    captured = capsys.readouterr()
    assert "Script Mode Works!" in captured.out


def test_cli_new_scaffolding_and_run(tmp_path: Path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    code = main(["new", "demo-app"])
    assert code == 0

    project_dir = tmp_path / "demo-app"
    assert (project_dir / "conf.clr").is_file()
    assert (project_dir / "src" / "main.clr").is_file()
    assert (project_dir / "tests" / "main_test.clr").is_file()
    assert (project_dir / "README.md").is_file()

    # cd into demo-app and run clarity run
    monkeypatch.chdir(project_dir)
    code_run = main(["run"])
    assert code_run == 0
    captured = capsys.readouterr()
    assert "Hello, Clarity!" in captured.out

    # run clarity test
    code_test = main(["test"])
    assert code_test == 0
    captured_test = capsys.readouterr()
    assert "Status: PASSED" in captured_test.out


def test_cli_new_rejects_invalid_name(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    code = main(["new", "invalid name with spaces"])
    assert code == 2

    # Existing non-empty directory
    existing = tmp_path / "existing"
    existing.mkdir()
    (existing / "somefile.txt").write_text("data")
    code_exist = main(["new", "existing"])
    assert code_exist == 1


def test_cli_run_explicit_entry(tmp_path: Path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    main(["new", "app"])
    app_dir = tmp_path / "app"
    (app_dir / "src" / "custom.clr").write_text('say "Custom Entry"', encoding="utf-8")

    monkeypatch.chdir(app_dir)
    code = main(["run", "src/custom.clr"])
    assert code == 0
    captured = capsys.readouterr()
    assert "Custom Entry" in captured.out


def test_cli_run_no_project_error(tmp_path: Path, monkeypatch, capsys):
    empty = tmp_path / "empty"
    empty.mkdir()
    monkeypatch.chdir(empty)
    code = main(["run"])
    assert code == 2
    captured = capsys.readouterr()
    assert "No Clarity project found" in captured.out


def test_test_runner_discovery_and_failure_isolation(tmp_path: Path):
    tests_dir = tmp_path / "tests"
    tests_dir.mkdir()

    test_file = tests_dir / "sample_test.clr"
    test_file.write_text(
        'function test_pass_1 {\n'
        '    assert_equal(1 + 1, 2, "1 + 1 should be 2")\n'
        '}\n\n'
        'function test_failing {\n'
        '    assert_equal(2 + 2, 5, "2 + 2 should be 4")\n'
        '}\n\n'
        'function test_pass_2 {\n'
        '    assert(true, "true should be true")\n'
        '}\n',
        encoding="utf-8",
    )

    discovered = discover_test_files(tests_dir)
    assert len(discovered) == 1

    results = run_test_file(test_file)
    assert len(results) == 3
    assert results[0].test_name == "test_failing"
    assert results[0].passed is False
    assert "Expected: 5" in (results[0].error_message or "")
    assert results[1].test_name == "test_pass_1"
    assert results[1].passed is True
    assert results[2].test_name == "test_pass_2"
    assert results[2].passed is True

    # Summary output
    out = io.StringIO()
    summary = run_tests(target_path=tests_dir, output_stream=out)
    assert summary.total == 3
    assert summary.passed_count == 2
    assert summary.failed_count == 1
    assert summary.is_success is False
    output_str = out.getvalue()
    assert "2 passed, 1 failed, 3 total" in output_str
    assert "Status: FAILED" in output_str


def test_stdlib_assert_functions():
    stdlib = get_standard_library()
    assert_fn = stdlib["assert"]
    assert_equal_fn = stdlib["assert_equal"]

    # Passing assertions
    assert_fn.call([True, "ok"])
    assert_equal_fn.call([42, 42, "should match"])

    # Failing assertions
    with pytest.raises(Exception, match="Assertion failed: custom error"):
        assert_fn.call([False, "custom error"])

    with pytest.raises(Exception, match="Assertion failed: mismatch\n  Expected: 10\n  Actual:   5"):
        assert_equal_fn.call([5, 10, "mismatch"])
