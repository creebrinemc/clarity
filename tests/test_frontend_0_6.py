"""Tests for Clarity 0.6 frontend: imports and member access parsing."""

import pytest
from clarity.lexer import Lexer
from clarity.parser import Parser
from clarity.errors import ParserError
from clarity.tokens import TokenType
import clarity.ast as ast


def parse_code(source: str):
    tokens = Lexer(source).tokenize()
    return Parser(tokens).parse()


def test_lexer_dot_and_keywords():
    tokens = Lexer('import "utils" as u\nfrom "math" import add\nuser.name').tokenize()
    types = [t.type for t in tokens if t.type not in (TokenType.NEWLINE, TokenType.EOF)]
    assert types == [
        TokenType.KEYWORD, TokenType.STRING, TokenType.KEYWORD, TokenType.IDENTIFIER,
        TokenType.KEYWORD, TokenType.STRING, TokenType.KEYWORD, TokenType.IDENTIFIER,
        TokenType.IDENTIFIER, TokenType.DOT, TokenType.IDENTIFIER
    ]


def test_parse_import_module():
    tree = parse_code('import "utils/formatting" as fmt')
    assert len(tree.statements) == 1
    stmt = tree.statements[0]
    assert isinstance(stmt, ast.ImportModuleNode)
    assert stmt.module_path == "utils/formatting"
    assert stmt.alias == "fmt"


def test_parse_from_import_comma_and():
    tree = parse_code('from "utils" import format_name, capitalize')
    assert len(tree.statements) == 1
    stmt = tree.statements[0]
    assert isinstance(stmt, ast.FromImportNode)
    assert stmt.module_path == "utils"
    assert len(stmt.items) == 2
    assert stmt.items[0].name == "format_name"
    assert stmt.items[0].alias is None
    assert stmt.items[1].name == "capitalize"
    assert stmt.items[1].alias is None

    # Test 'and' keyword separator
    tree2 = parse_code('from "utils" import format_name and capitalize')
    stmt2 = tree2.statements[0]
    assert isinstance(stmt2, ast.FromImportNode)
    assert len(stmt2.items) == 2


def test_parse_from_import_with_aliases():
    tree = parse_code('from "utils" import format_name as fn, capitalize as cap')
    stmt = tree.statements[0]
    assert isinstance(stmt, ast.FromImportNode)
    assert stmt.items[0].name == "format_name"
    assert stmt.items[0].alias == "fn"
    assert stmt.items[1].name == "capitalize"
    assert stmt.items[1].alias == "cap"


def test_parse_member_access():
    tree = parse_code('say user.name')
    stmt = tree.statements[0]
    assert isinstance(stmt, ast.PrintNode)
    assert isinstance(stmt.expression, ast.MemberAccessNode)
    assert isinstance(stmt.expression.target, ast.IdentifierNode)
    assert stmt.expression.target.name == "user"
    assert stmt.expression.member == "name"


def test_parse_chained_member_access_and_call():
    tree = parse_code('fmt.format_name("alice")')
    stmt = tree.statements[0]
    assert isinstance(stmt, ast.ExpressionStatementNode)
    assert isinstance(stmt.expression, ast.CallNode)
    assert isinstance(stmt.expression.callee, ast.MemberAccessNode)
    assert stmt.expression.callee.target.name == "fmt"
    assert stmt.expression.callee.member == "format_name"


def test_parse_import_errors():
    with pytest.raises(ParserError, match="Whole-module import requires an alias with 'as'"):
        parse_code('import "utils"')

    with pytest.raises(ParserError, match="Expected module path string after 'import'"):
        parse_code('import utils as u')

    with pytest.raises(ParserError, match="Expected 'import' after module path"):
        parse_code('from "utils" as u')


def test_dot_mutation_rejected():
    with pytest.raises(ParserError, match="Expected variable name or index target after 'set'"):
        parse_code('set user.name to "Bob"')
