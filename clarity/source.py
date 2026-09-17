"""Source-coordinate value objects shared by the language frontend."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SourceSpan:
    """An inclusive start and exclusive end position in a source file."""

    start_line: int
    start_column: int
    end_line: int
    end_column: int

    def cover(self, other: "SourceSpan") -> "SourceSpan":
        """Return the smallest span covering this span and ``other``."""
        return SourceSpan(self.start_line, self.start_column, other.end_line, other.end_column)
