"""Native Clarity test runner discovering and executing project test suites."""

import time
from dataclasses import dataclass
from pathlib import Path
from typing import TextIO

from .errors import ClarityError
from .evaluator import Evaluator
from .lexer import Lexer
from .modules import ModuleManager
from .parser import Parser
from .project import ProjectConfig, discover_project
from .runtime import ClarityFunction


@dataclass(slots=True)
class TestResult:
    file_path: Path
    test_name: str
    passed: bool
    duration_ms: float
    error_message: str | None = None


@dataclass(slots=True)
class TestSuiteSummary:
    results: list[TestResult]
    total_time_ms: float

    @property
    def total(self) -> int:
        return len(self.results)

    @property
    def passed_count(self) -> int:
        return sum(1 for r in self.results if r.passed)

    @property
    def failed_count(self) -> int:
        return sum(1 for r in self.results if not r.passed)

    @property
    def is_success(self) -> bool:
        return self.failed_count == 0


def discover_test_files(target_path: Path) -> list[Path]:
    """Discover all *_test.clr and test_*.clr files in the given directory or file."""
    p = target_path.resolve()
    if p.is_file():
        if p.name.endswith(".clr"):
            return [p]
        return []

    if not p.is_dir():
        return []

    discovered: list[Path] = []
    for file_path in p.rglob("*.clr"):
        name = file_path.name
        if (name.endswith("_test.clr") or name.startswith("test_")) and not name.startswith("."):
            discovered.append(file_path.resolve())

    return sorted(discovered)


def run_test_file(
    file_path: Path,
    project_root: Path | None = None,
    output_fn=None,
) -> list[TestResult]:
    """Execute a single test file using Model D (Hybrid Top-Level + test_* execution)."""
    file_path = file_path.resolve()
    try:
        source = file_path.read_text(encoding="utf-8")
    except OSError as err:
        return [
            TestResult(
                file_path=file_path,
                test_name="(load)",
                passed=False,
                duration_ms=0.0,
                error_message=f"Could not read test file: {err}",
            )
        ]

    manager = ModuleManager(project_root=project_root, output=output_fn)
    evaluator = Evaluator(
        module_manager=manager,
        current_file=file_path,
        project_root=project_root,
        output=output_fn or (lambda _: None),
    )

    t_start = time.perf_counter()
    try:
        tokens = Lexer(source).tokenize()
        tree = Parser(tokens).parse()
        evaluator.evaluate(tree)
    except ClarityError as err:
        t_duration = (time.perf_counter() - t_start) * 1000.0
        return [
            TestResult(
                file_path=file_path,
                test_name="(top-level)",
                passed=False,
                duration_ms=t_duration,
                error_message=str(err),
            )
        ]
    except Exception as err:
        t_duration = (time.perf_counter() - t_start) * 1000.0
        return [
            TestResult(
                file_path=file_path,
                test_name="(top-level)",
                passed=False,
                duration_ms=t_duration,
                error_message=f"Unexpected error: {err}",
            )
        ]

    # Discover test_* functions
    test_functions: list[tuple[str, ClarityFunction]] = []
    for name, value in evaluator.environment.values.items():
        if name.startswith("test_") and isinstance(value, ClarityFunction):
            test_functions.append((name, value))

    # Sort test functions deterministically
    test_functions.sort(key=lambda item: item[0])

    if not test_functions:
        # Top-level script execution was the test
        t_duration = (time.perf_counter() - t_start) * 1000.0
        return [
            TestResult(
                file_path=file_path,
                test_name="(script)",
                passed=True,
                duration_ms=t_duration,
            )
        ]

    results: list[TestResult] = []
    for func_name, func in test_functions:
        f_start = time.perf_counter()
        try:
            evaluator._call_function(func, [])
            f_duration = (time.perf_counter() - f_start) * 1000.0
            results.append(
                TestResult(
                    file_path=file_path,
                    test_name=func_name,
                    passed=True,
                    duration_ms=f_duration,
                )
            )
        except ClarityError as err:
            f_duration = (time.perf_counter() - f_start) * 1000.0
            results.append(
                TestResult(
                    file_path=file_path,
                    test_name=func_name,
                    passed=False,
                    duration_ms=f_duration,
                    error_message=str(err),
                )
            )
        except Exception as err:
            f_duration = (time.perf_counter() - f_start) * 1000.0
            results.append(
                TestResult(
                    file_path=file_path,
                    test_name=func_name,
                    passed=False,
                    duration_ms=f_duration,
                    error_message=f"Unexpected error: {err}",
                )
            )

    return results


def run_tests(
    target_path: Path | None = None,
    project_config: ProjectConfig | None = None,
    output_stream: TextIO | None = None,
) -> TestSuiteSummary:
    """Run all discovered tests and format reporting."""
    import sys
    out = output_stream or sys.stdout

    start_dir = target_path or Path.cwd()
    if project_config is None:
        project_config = discover_project(start_dir)

    project_root = project_config.root if project_config else None

    # Determine discovery path
    if target_path is not None:
        discovery_target = target_path
    elif project_config and (project_config.root / "tests").is_dir():
        discovery_target = project_config.root / "tests"
    else:
        discovery_target = Path.cwd() / "tests" if (Path.cwd() / "tests").is_dir() else Path.cwd()

    test_files = discover_test_files(discovery_target)

    header = "Clarity Test Runner"
    if project_config:
        header += f" — {project_config.name} (v{project_config.version})"
    out.write(f"{header}\n")
    if project_root:
        out.write(f"Root: {project_root.as_posix()}\n\n")
    else:
        out.write(f"Target: {discovery_target.as_posix()}\n\n")

    if not test_files:
        out.write("No test files found (*_test.clr, test_*.clr).\n\n")
        out.write("Tests:  0 total\n")
        out.write("Status: PASSED\n")
        return TestSuiteSummary(results=[], total_time_ms=0.0)

    all_results: list[TestResult] = []
    suite_start = time.perf_counter()

    for test_file in test_files:
        rel_path = (test_file.relative_to(project_root) if project_root and test_file.is_relative_to(project_root) else test_file).as_posix()
        file_results = run_test_file(test_file, project_root=project_root)
        all_results.extend(file_results)

        for res in file_results:
            duration_str = f"[{res.duration_ms:.1f}ms]"
            if res.passed:
                out.write(f"  ✓ {rel_path} > {res.test_name} {duration_str}\n")
            else:
                out.write(f"  ✗ {rel_path} > {res.test_name} {duration_str}\n")
                if res.error_message:
                    indented = "\n".join(f"    {line}" for line in res.error_message.splitlines())
                    out.write(f"{indented}\n")

    total_time_ms = (time.perf_counter() - suite_start) * 1000.0

    summary = TestSuiteSummary(results=all_results, total_time_ms=total_time_ms)
    out.write("\n" + "-" * 55 + "\n")
    out.write(f"Tests:  {summary.passed_count} passed, {summary.failed_count} failed, {summary.total} total\n")
    out.write(f"Time:   {summary.total_time_ms:.1f}ms\n")
    out.write(f"Status: {'PASSED' if summary.is_success else 'FAILED'}\n")

    return summary
