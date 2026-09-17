import pytest

from clarity.errors import LexerError
from clarity.lexer import Lexer
from clarity.tokens import TokenType


def tokens(source): return Lexer(source).tokenize()


def test_variables_numbers_and_keywords():
    result = tokens("set score to 14")
    assert [(t.type, t.value) for t in result[:-1]] == [
        (TokenType.KEYWORD, "set"), (TokenType.IDENTIFIER, "score"),
        (TokenType.KEYWORD, "to"), (TokenType.NUMBER, 14),
    ]


def test_strings_operators_and_comments():
    result = tokens('say "hi" + 2 # ignored\n')
    assert [t.value for t in result[:-1]] == ["say", "hi", "+", 2, "\n"]
    assert result[2].type is TokenType.OPERATOR


def test_line_and_column_tracking():
    result = tokens("\n  say true\n")
    say, boolean = result[1], result[2]
    assert (say.line, say.column) == (2, 3)
    assert (boolean.line, boolean.column) == (2, 7)


def test_invalid_character_has_source_location():
    with pytest.raises(LexerError, match=r"Unexpected character '\$'") as error:
        tokens("say $\n")
    assert (error.value.line, error.value.column) == (1, 5)


@pytest.mark.parametrize(
    ("source", "message"),
    [
        ('say "unfinished', "Unterminated string"),
        ('say "unfinished\\', "escape sequence is incomplete"),
        ('say "first\nsecond"', "Unterminated string"),
    ],
)
def test_malformed_strings_raise_lexer_errors(source, message):
    with pytest.raises(LexerError, match=message) as error:
        tokens(source)
    assert (error.value.line, error.value.column) == (1, 5)


def test_string_escapes_are_lexed():
    result = tokens(r'say "a\"quote\" and \\ slash"')
    assert result[1].value == 'a"quote" and \\ slash'
