import pytest

from clarity import ast
from clarity.errors import ParserError
from clarity.lexer import Lexer
from clarity.parser import Parser


def parse(source): return Parser(Lexer(source).tokenize()).parse()


def test_assignment_and_say():
    program = parse('set name to "Clarity"\nsay name\n')
    assert isinstance(program.statements[0], ast.AssignNode)
    assert program.statements[0].name == "name"
    assert isinstance(program.statements[1], ast.PrintNode)


def test_arithmetic_precedence_and_parentheses():
    expression = parse("say 2 + 3 * 4\n").statements[0].expression
    assert expression.operator == "+"
    assert expression.right.operator == "*"
    grouped = parse("say (2 + 3) * 4\n").statements[0].expression
    assert grouped.operator == "*"
    assert grouped.left.operator == "+"


def test_identifiers_lists_and_dictionaries():
    program = parse('set items to [name, 2]\nset user to {"name": name}\n')
    assert isinstance(program.statements[0].expression, ast.ListNode)
    assert isinstance(program.statements[0].expression.elements[0], ast.IdentifierNode)
    dictionary = program.statements[1].expression
    assert isinstance(dictionary, ast.DictionaryNode)
    assert len(dictionary.entries) == 1


def test_empty_collection_literals_parse():
    program = parse("set items to []\nset metadata to {}\n")
    assert program.statements[0].expression.elements == []
    assert program.statements[1].expression.entries == []


def test_push_and_pop_parse_as_dedicated_nodes():
    program = parse('push "Potion" to inventory\npop from inventory\n')
    assert isinstance(program.statements[0], ast.PushNode)
    assert isinstance(program.statements[1], ast.PopNode)


def test_unary_nodes_and_mixed_precedence():
    expression = parse("say not -+2 < 3 and false or true\n").statements[0].expression
    assert expression.operator == "or"
    assert expression.left.operator == "and"
    comparison = expression.left.left
    assert comparison.operator == "<"
    assert comparison.left.operator == "not"
    assert comparison.left.operand.operator == "-"
    assert comparison.left.operand.operand.operator == "+"


def test_binary_operations_are_left_associative():
    expression = parse("say 10 - 3 - 2\n").statements[0].expression
    assert expression.operator == "-"
    assert expression.left.operator == "-"


@pytest.mark.parametrize(
    ("source", "message"),
    [
        ("set score 10\n", "Expected 'to'"),
        ("set score to 1 +\n", "Expected an expression"),
        ("say (1 + 2\n", r"Expected '\)'"),
        ("unknown statement\n", "Expected a statement"),
        ("say 1 say 2\n", "Expected a newline"),
    ],
)
def test_parser_reports_meaningful_malformed_syntax(source, message):
    with pytest.raises(ParserError, match=message):
        parse(source)


def test_ast_nodes_preserve_source_spans():
    program = parse("set result to (2 + 3) * 4\n")
    assignment = program.statements[0]
    expression = assignment.expression
    assert (assignment.span.start_line, assignment.span.start_column) == (1, 1)
    assert (assignment.span.end_line, assignment.span.end_column) == (1, 26)
    assert (expression.span.start_column, expression.span.end_column) == (15, 26)
