"""Module resolution, loading, caching, and cycle detection for Clarity."""

from pathlib import Path
from typing import TYPE_CHECKING

from .errors import CircularImportError, ModuleError, ClarityError
from .lexer import Lexer
from .parser import Parser
from .runtime import ClarityModule
from .source import SourceSpan

if TYPE_CHECKING:
    from .environment import Environment
    from .evaluator import Evaluator


class ModuleManager:
    """Manages module discovery, singleton evaluation, and circular dependency tracking."""

    def __init__(self, project_root: Path | None = None, output=None):
        self.project_root = project_root.resolve() if project_root else None
        self.output = output
        self.module_cache: dict[Path, ClarityModule] = {}
        self.loading_stack: list[tuple[Path, SourceSpan | None]] = []

    def resolve(
        self,
        specifier: str,
        importing_file: Path | None = None,
        span: SourceSpan | None = None,
    ) -> Path:
        """Resolve a module specifier string to an absolute canonical Path."""
        clean_spec = specifier.strip().replace("\\", "/")
        if clean_spec.endswith(".clr"):
            clean_spec = clean_spec[:-4]

        searched_paths: list[Path] = []

        # 1. Relative imports (starts with ./ or ../)
        if clean_spec.startswith("./") or clean_spec.startswith("../"):
            base_dir = importing_file.parent if importing_file else Path.cwd()
            candidates = [
                base_dir / f"{clean_spec}.clr",
                base_dir / clean_spec / "main.clr",
                base_dir / clean_spec / "mod.clr",
            ]
            for candidate in candidates:
                searched_paths.append(candidate)
                if candidate.is_file():
                    return candidate.resolve()
            self._raise_not_found(specifier, searched_paths, importing_file, span)

        # 2. Project-root relative imports (when project_root is present)
        if self.project_root:
            candidates = [
                self.project_root / "src" / f"{clean_spec}.clr",
                self.project_root / f"{clean_spec}.clr",
                self.project_root / "src" / clean_spec / "main.clr",
                self.project_root / "src" / clean_spec / "mod.clr",
                self.project_root / clean_spec / "main.clr",
                self.project_root / clean_spec / "mod.clr",
            ]
            for candidate in candidates:
                searched_paths.append(candidate)
                if candidate.is_file():
                    return candidate.resolve()

        # 3. Importing-file relative fallback (script mode or local imports without ./ prefix)
        if importing_file:
            candidates = [
                importing_file.parent / f"{clean_spec}.clr",
                importing_file.parent / clean_spec / "main.clr",
                importing_file.parent / clean_spec / "mod.clr",
            ]
            for candidate in candidates:
                if candidate not in searched_paths:
                    searched_paths.append(candidate)
                if candidate.is_file():
                    return candidate.resolve()

        # 4. Current working directory fallback
        cwd = Path.cwd()
        candidates = [
            cwd / f"{clean_spec}.clr",
            cwd / clean_spec / "main.clr",
            cwd / clean_spec / "mod.clr",
        ]
        for candidate in candidates:
            if candidate not in searched_paths:
                searched_paths.append(candidate)
            if candidate.is_file():
                return candidate.resolve()

        self._raise_not_found(specifier, searched_paths, importing_file, span)

    def load_module(
        self,
        module_path: Path,
        span: SourceSpan | None = None,
        evaluator_factory=None,
    ) -> ClarityModule:
        """Load, evaluate, and cache a module at the given path with cycle detection."""
        resolved = module_path.resolve()

        if resolved in self.module_cache:
            return self.module_cache[resolved]

        # Cycle detection
        active_paths = [p for p, _ in self.loading_stack]
        if resolved in active_paths:
            cycle_idx = active_paths.index(resolved)
            cycle_chain = active_paths[cycle_idx:] + [resolved]
            chain_str = " -> ".join(
                (p.relative_to(self.project_root) if self.project_root and p.is_relative_to(self.project_root) else Path(p.name)).as_posix()
                for p in cycle_chain
            )
            message = f"Detected circular dependency:\n  {chain_str}"
            raise CircularImportError(message, span)

        if not resolved.is_file():
            raise ModuleError(f"Cannot read module file: {resolved}", span)

        try:
            source = resolved.read_text(encoding="utf-8")
        except OSError as err:
            raise ModuleError(f"Could not read module {resolved}: {err}", span)

        tokens = Lexer(source).tokenize()
        ast_tree = Parser(tokens).parse()

        # Lazy import of Evaluator if not provided
        if evaluator_factory is None:
            from .evaluator import Evaluator
            evaluator_factory = Evaluator

        self.loading_stack.append((resolved, span))
        try:
            # Create fresh evaluator with clean isolated environment sharing this module manager
            evaluator = evaluator_factory(
                module_manager=self,
                current_file=resolved,
                project_root=self.project_root,
                output=self.output,
            )
            evaluator.evaluate(ast_tree)
            module = ClarityModule(
                name=resolved.stem,
                file_path=resolved,
                environment=evaluator.environment,
            )
            self.module_cache[resolved] = module
            return module
        finally:
            self.loading_stack.pop()

    def _raise_not_found(
        self,
        specifier: str,
        searched: list[Path],
        importing_file: Path | None,
        span: SourceSpan | None,
    ) -> None:
        searched_lines = "\n".join(
            f"  - {(p.relative_to(self.project_root) if self.project_root and p.is_relative_to(self.project_root) else p).as_posix()}"
            for p in searched
        )
        imported_from = f"\nImported from: {importing_file.as_posix()}" if importing_file else ""
        msg = (
            f"Could not find module \"{specifier}\".{imported_from}\n\n"
            f"Searched locations:\n{searched_lines}"
        )
        raise ModuleError(msg, span)
