"""User-facing diagnostic errors for Clarity."""

from .source import SourceSpan


class ClarityError(Exception):
    category = "Error"

    def __init__(self, message: str, span: SourceSpan | None = None):
        self.message, self.span = message, span
        super().__init__(message)

    @property
    def line(self) -> int | None:
        return self.span.start_line if self.span else None

    @property
    def column(self) -> int | None:
        return self.span.start_column if self.span else None

    def with_span(self, span: SourceSpan) -> "ClarityError":
        if self.span is None:
            self.span = span
        return self

    def __str__(self) -> str:
        location = ""
        if self.span is not None:
            location = f"\n\nLine {self.line}, column {self.column}"
        return f"Clarity {self.category} Error\n\n{self.message}{location}"


class LexerError(ClarityError):
    category = "Lexer"


class ParserError(ClarityError):
    category = "Parser"


class RuntimeError(ClarityError):
    category = "Runtime"
