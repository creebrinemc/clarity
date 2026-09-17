"""A hand-written lexer for Clarity source code."""

from .errors import LexerError
from .source import SourceSpan
from .tokens import Token, TokenType

KEYWORDS = {
    "set", "to", "say", "push", "pop", "from", "and", "or", "not",
    "if", "else", "while", "for", "in", "step", "break", "continue",
    "function", "taking", "return",
    "each", "repeat", "times", "is", "equal", "greater", "less", "than",
    "at", "least", "most",
}
BOOLEAN_WORDS = {"true": True, "false": False}
NULL_WORDS = {"nothing", "null"}


class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.current = 0
        self.line = 1
        self.column = 1

    def tokenize(self) -> list[Token]:
        tokens: list[Token] = []
        while not self._at_end():
            char = self._peek()
            if char in " \t\r":
                self._advance()
            elif char == "\n":
                line, column = self.line, self.column
                self._advance_line()
                tokens.append(Token(TokenType.NEWLINE, "\n", SourceSpan(line, column, self.line, self.column)))
            elif char == "#":
                self._skip_comment()
            elif char.isdigit():
                tokens.append(self._number())
            elif char.isalpha() or char == "_":
                tokens.append(self._identifier())
            elif char == '"':
                tokens.append(self._string())
            else:
                tokens.append(self._symbol())
        tokens.append(Token(TokenType.EOF, None, SourceSpan(self.line, self.column, self.line, self.column)))
        return tokens

    def _symbol(self) -> Token:
        line, column = self.line, self.column
        char = self._advance()
        singles = {"(": TokenType.LEFT_PAREN, ")": TokenType.RIGHT_PAREN,
                   "[": TokenType.LEFT_BRACKET, "]": TokenType.RIGHT_BRACKET,
                   "{": TokenType.LEFT_BRACE, "}": TokenType.RIGHT_BRACE,
                   ",": TokenType.COMMA, ":": TokenType.COLON}
        if char in singles:
            return self._completed_token(singles[char], char, line, column)
        if char in "+-*/%":
            return self._completed_token(TokenType.OPERATOR, char, line, column)
        if char in "=!><":
            value = char + self._advance() if self._peek() == "=" else char
            if value in {"=", "!"}:
                raise LexerError(f"Unexpected character {char!r}", SourceSpan(line, column, self.line, self.column))
            return self._completed_token(TokenType.OPERATOR, value, line, column)
        raise LexerError(f"Unexpected character {char!r}", SourceSpan(line, column, self.line, self.column))

    def _number(self) -> Token:
        line, column, start = self.line, self.column, self.current
        while self._peek().isdigit(): self._advance()
        if self._peek() == "." and self._peek_next().isdigit():
            self._advance()
            while self._peek().isdigit(): self._advance()
        raw = self.source[start:self.current]
        value = float(raw) if "." in raw else int(raw)
        return self._completed_token(TokenType.NUMBER, value, line, column)

    def _identifier(self) -> Token:
        line, column, start = self.line, self.column, self.current
        while self._peek().isalnum() or self._peek() == "_": self._advance()
        value = self.source[start:self.current]
        if value in BOOLEAN_WORDS: return self._completed_token(TokenType.BOOLEAN, BOOLEAN_WORDS[value], line, column)
        if value in NULL_WORDS: return self._completed_token(TokenType.NULL, None, line, column)
        return self._completed_token(TokenType.KEYWORD if value in KEYWORDS else TokenType.IDENTIFIER, value, line, column)

    def _string(self) -> Token:
        line, column = self.line, self.column
        self._advance()  # opening quote
        chars: list[str] = []
        while not self._at_end() and self._peek() != '"':
            if self._peek() == "\n":
                raise LexerError("Unterminated string", SourceSpan(line, column, self.line, self.column))
            if self._peek() == "\\":
                self._advance()
                if self._at_end():
                    raise LexerError(
                        "Unterminated string: escape sequence is incomplete",
                        SourceSpan(line, column, self.line, self.column),
                    )
                escapes = {"n": "\n", "t": "\t", '"': '"', "\\": "\\"}
                chars.append(escapes.get(self._advance(), self.source[self.current - 1]))
            else: chars.append(self._advance())
        if self._at_end(): raise LexerError("Unterminated string", SourceSpan(line, column, self.line, self.column))
        self._advance()
        return self._completed_token(TokenType.STRING, "".join(chars), line, column)

    def _skip_comment(self) -> None:
        while not self._at_end() and self._peek() != "\n": self._advance()

    def _completed_token(self, kind: TokenType, value: object, line: int, column: int) -> Token:
        return Token(kind, value, SourceSpan(line, column, self.line, self.column))
    def _at_end(self) -> bool: return self.current >= len(self.source)
    def _peek(self) -> str: return "\0" if self._at_end() else self.source[self.current]
    def _peek_next(self) -> str: return "\0" if self.current + 1 >= len(self.source) else self.source[self.current + 1]
    def _advance(self) -> str:
        char = self.source[self.current]; self.current += 1; self.column += 1; return char
    def _advance_line(self) -> None: self.current += 1; self.line += 1; self.column = 1
