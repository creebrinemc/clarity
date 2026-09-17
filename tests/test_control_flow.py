import pytest

from clarity import ast
from clarity.errors import ParserError, RuntimeError
from clarity.evaluator import Evaluator
from clarity.lexer import Lexer
from clarity.parser import Parser


def parse(source: str) -> ast.ProgramNode:
    return Parser(Lexer(source).tokenize()).parse()


def execute(source: str):
    output: list[str] = []
    evaluator = Evaluator(output=output.append)
    evaluator.evaluate(parse(source))
    return evaluator.environment, output


def test_empty_and_nested_blocks_have_lexical_scopes():
    environment, output = execute(
        "{}\n"
        "set value to 1\n"
        "{\n"
        "  set value to 2\n"
        "  {\n"
        "    set value to 3\n"
        "    set local to \"inside\"\n"
        "  }\n"
        "  say value\n"
        "}\n"
        "say value\n"
    )
    assert output == ["3", "3"]
    assert environment.get("value") == 3
    with pytest.raises(RuntimeError, match="Unknown variable: local"):
        environment.get("local")


def test_if_else_if_and_else_execute_only_first_matching_branch():
    _, output = execute(
        "set score to 85\n"
        "if score >= 90 {\n"
        "  say \"excellent\"\n"
        "} else if score >= 70 {\n"
        "  say \"good\"\n"
        "} else {\n"
        "  say \"practice\"\n"
        "}\n"
    )
    assert output == ["good"]


def test_if_supports_multiple_else_if_branches_nested_conditions_and_comments():
    _, output = execute(
        "set value to 2\n"
        "if value == 1 {\n"
        "  say \"one\"\n"
        "} else if value == 2 {\n"
        "  # Nested blocks allow blank lines.\n"
        "\n"
        "  if true { say \"two\" }\n"
        "} else if value == 3 {\n"
        "  say \"three\"\n"
        "} else {\n"
        "  say \"other\"\n"
        "}\n"
    )
    assert output == ["two"]


def test_if_conditions_use_clarity_truthiness_and_support_else_on_next_line():
    _, output = execute(
        "if 0 { say \"zero is truthy\" }\n"
        "if false {\n"
        "  say \"wrong\"\n"
        "}\n"
        "else {\n"
        "  say \"fallback\"\n"
        "}\n"
    )
    assert output == ["zero is truthy", "fallback"]


def test_while_reevaluates_condition_and_can_have_zero_iterations():
    _, output = execute(
        "set count to 0\n"
        "while count < 3 {\n"
        "  say count\n"
        "  set count to count + 1\n"
        "}\n"
        "while false { say \"never\" }\n"
    )
    assert output == ["0", "1", "2"]


def test_nested_while_loops_execute_independently():
    _, output = execute(
        "set outer to 0\n"
        "while outer < 2 {\n"
        "  set inner to 0\n"
        "  while inner < 1 {\n"
        "    say outer\n"
        "    set inner to inner + 1\n"
        "  }\n"
        "  set outer to outer + 1\n"
        "}\n"
    )
    assert output == ["0", "1"]


def test_for_in_iterates_lists_strings_and_keeps_loop_variable_local():
    environment, output = execute(
        "set item to \"outer\"\n"
        "set values to [\"a\", \"b\"]\n"
        "for item in values { say item }\n"
        "for letter in \"xy\" { say letter }\n"
        "for nothing_here in [] { say nothing_here }\n"
        "say item\n"
    )
    assert output == ["a", "b", "x", "y", "outer"]
    assert environment.get("item") == "outer"
    with pytest.raises(RuntimeError, match="Unknown variable: letter"):
        environment.get("letter")


def test_range_loops_are_inclusive_ascending_descending_and_support_step():
    _, output = execute(
        "for number from 1 to 3 { say number }\n"
        "for number from 5 to 1 { say number }\n"
        "for number from 1 to 5 step 2 { say number }\n"
        "for number from 5 to 1 step 2 { say number }\n"
    )
    assert output == ["1", "2", "3", "5", "4", "3", "2", "1", "1", "3", "5", "5", "3", "1"]


def test_break_and_continue_apply_to_nearest_loop():
    _, output = execute(
        "set count to 0\n"
        "while true {\n"
        "  set count to count + 1\n"
        "  if count == 2 { continue }\n"
        "  say count\n"
        "  if count == 3 { break }\n"
        "}\n"
        "for outer from 1 to 2 {\n"
        "  for inner from 1 to 3 {\n"
        "    if inner == 2 { break }\n"
        "    say inner\n"
        "  }\n"
        "}\n"
    )
    assert output == ["1", "3", "1", "1"]


def test_continue_in_a_nested_for_loop_does_not_continue_the_outer_loop():
    _, output = execute(
        "for outer from 1 to 2 {\n"
        "  for inner from 1 to 3 {\n"
        "    if inner == 2 { continue }\n"
        "    say inner\n"
        "  }\n"
        "  say \"outer done\"\n"
        "}\n"
    )
    assert output == ["1", "3", "outer done", "1", "3", "outer done"]


@pytest.mark.parametrize(
    ("source", "message"),
    [
        ("break\n", "only be used inside a loop"),
        ("continue\n", "only be used inside a loop"),
        ("for value from 1 to 2 step 0 { say value }\n", "must not be zero"),
        ("for value in 12 { say value }\n", "require a list or string"),
        ("for value from true to 2 { say value }\n", "Range start requires a number"),
        ("if true { say unknown }\n", "Unknown variable"),
    ],
)
def test_control_flow_runtime_errors_keep_source_locations(source, message):
    with pytest.raises(RuntimeError, match=message) as error:
        execute(source)
    assert error.value.line == 1
    assert error.value.column is not None


@pytest.mark.parametrize(
    ("source", "message"),
    [
        ("if true\n", "Expected '{' after if condition"),
        ("if true {\n", "Expected '}' to close block"),
        ("}\n", "Unexpected '}' outside a block"),
        ("else { }\n", "Expected a statement"),
        ("while { }\n", "Expected '{' after while condition"),
        ("for item values { }\n", "Expected 'in' or 'from'"),
        ("for item from 1 3 { }\n", "Expected 'to'"),
        ("for item from 1 to 3 step { }\n", "Expected '{' after range loop"),
        ("if true { } else say \"no\"\n", "Expected 'if' or '{' after 'else'"),
    ],
)
def test_control_flow_parser_errors_are_clear(source, message):
    with pytest.raises(ParserError, match=message):
        parse(source)


def test_control_flow_ast_nodes_and_spans():
    program = parse("if true { for item in [1] { break } }\n")
    if_node = program.statements[0]
    assert isinstance(if_node, ast.IfNode)
    assert isinstance(if_node.then_block.statements[0], ast.ForInNode)
    assert if_node.span.start_column == 1
    assert if_node.span.end_column == 38


def test_empty_block_is_represented_in_the_ast():
    block = parse("{}\n").statements[0]
    assert isinstance(block, ast.BlockNode)
    assert block.statements == []


def test_complete_control_flow_program_integration():
    _, output = execute(
        "set total to 0\n"
        "for number from 1 to 5 {\n"
        "  if number == 3 { continue }\n"
        "  set total to total + number\n"
        "}\n"
        "while total < 10 { set total to total + 1 }\n"
        "if total == 12 { say \"complete\" } else { say \"unexpected\" }\n"
    )
    assert output == ["complete"]
