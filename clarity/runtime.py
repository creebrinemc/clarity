"""Runtime-only Clarity values that do not belong in the AST."""

from dataclasses import dataclass
from typing import TYPE_CHECKING

from . import ast
from .source import SourceSpan

if TYPE_CHECKING:
    from .environment import Environment


@dataclass(slots=True)
class ClarityFunction:
    name: str | None
    parameters: tuple[ast.Parameter, ...]
    body: ast.BlockNode
    closure: "Environment"
    span: SourceSpan

    def display_name(self) -> str:
        return self.name or "anonymous"
