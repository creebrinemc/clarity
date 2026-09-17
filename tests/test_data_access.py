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


# ---------------------------------------------------------------------------
# List Indexing & Indexed Assignment
# ---------------------------------------------------------------------------


def test_list_indexing_reads_elements():
    _, output = execute(
        "set items to [\"a\", \"b\", \"c\"]\n"
        "say items[0]\n"
        "say items[1]\n"
        "say items[2]\n"
    )
    assert output == ["a", "b", "c"]


def test_list_indexed_assignment_updates_elements():
    _, output = execute(
        "set items to [\"a\", \"b\", \"c\"]\n"
        "set items[1] to \"x\"\n"
        "say items\n"
        "say items[1]\n"
    )
    assert output == ["[\"a\", \"x\", \"c\"]", "x"]


def test_list_indexing_with_computed_expression_indices():
    _, output = execute(
        "set items to [10, 20, 30, 40]\n"
        "set idx to 1 + 1\n"
        "say items[idx]\n"
        "set items[idx + 1] to 99\n"
        "say items\n"
    )
    assert output == ["30", "[10, 20, 30, 99]"]


# ---------------------------------------------------------------------------
# Dictionary Indexing & Assignment
# ---------------------------------------------------------------------------


def test_dictionary_indexing_with_quoted_and_unquoted_keys():
    _, output = execute(
        "set user to {\n"
        "  name: \"Creebrine\",\n"
        "  age: 14\n"
        "}\n"
        "say user[\"name\"]\n"
        "say user[\"age\"]\n"
    )
    assert output == ["Creebrine", "14"]


def test_dictionary_indexed_assignment_updates_and_adds_keys():
    _, output = execute(
        "set user to {\"name\": \"Creebrine\", \"age\": 14}\n"
        "set user[\"age\"] to 15\n"
        "set user[\"rank\"] to \"Admin\"\n"
        "say user[\"age\"]\n"
        "say user[\"rank\"]\n"
    )
    assert output == ["15", "Admin"]


def test_dictionary_with_numeric_and_boolean_keys():
    _, output = execute(
        "set table to { 1: \"one\", true: \"yes\", nothing: \"none\" }\n"
        "say table[1]\n"
        "say table[true]\n"
        "say table[nothing]\n"
    )
    assert output == ["one", "yes", "none"]


# ---------------------------------------------------------------------------
# Nested Indexing
# ---------------------------------------------------------------------------


def test_nested_list_and_dictionary_access():
    _, output = execute(
        "set users to [\n"
        "  { name: \"Alice\", scores: [90, 95] },\n"
        "  { name: \"Bob\", scores: [80, 85] }\n"
        "]\n"
        "say users[0][\"name\"]\n"
        "say users[0][\"scores\"][1]\n"
        "say users[1][\"name\"]\n"
    )
    assert output == ["Alice", "95", "Bob"]


def test_nested_indexed_assignment():
    _, output = execute(
        "set data to {\n"
        "  \"users\": [\n"
        "    { name: \"Alice\", tags: [\"dev\"] }\n"
        "  ]\n"
        "}\n"
        "set data[\"users\"][0][\"name\"] to \"Alicia\"\n"
        "set data[\"users\"][0][\"tags\"][0] to \"lead\"\n"
        "say data[\"users\"][0][\"name\"]\n"
        "say data[\"users\"][0][\"tags\"][0]\n"
    )
    assert output == ["Alicia", "lead"]


# ---------------------------------------------------------------------------
# String Indexing
# ---------------------------------------------------------------------------


def test_string_indexing():
    _, output = execute(
        "set word to \"Clarity\"\n"
        "say word[0]\n"
        "say word[3]\n"
        "say word[6]\n"
    )
    assert output == ["C", "r", "y"]


# ---------------------------------------------------------------------------
# English Comparison Aliases
# ---------------------------------------------------------------------------


def test_english_comparison_aliases():
    _, output = execute(
        "set age to 18\n"
        "set score to 85\n"
        "if age is equal to 18 { say \"equal\" }\n"
        "if age is not equal to 20 { say \"not equal\" }\n"
        "if score is greater than 80 { say \"greater\" }\n"
        "if score is less than 90 { say \"less\" }\n"
        "if age is at least 18 { say \"at least\" }\n"
        "if score is at most 85 { say \"at most\" }\n"
    )
    assert output == [
        "equal",
        "not equal",
        "greater",
        "less",
        "at least",
        "at most",
    ]


def test_english_comparisons_with_strings():
    _, output = execute(
        "set name to \"Clarity\"\n"
        "if name is equal to \"Clarity\" { say \"match\" }\n"
        "if name is not equal to \"Python\" { say \"diff\" }\n"
        "if \"b\" is greater than \"a\" { say \"alphabetical\" }\n"
    )
    assert output == ["match", "diff", "alphabetical"]


# ---------------------------------------------------------------------------
# `for each` Loops
# ---------------------------------------------------------------------------


def test_for_each_loop_over_list():
    _, output = execute(
        "set items to [\"red\", \"green\", \"blue\"]\n"
        "for each color in items {\n"
        "  say color\n"
        "}\n"
    )
    assert output == ["red", "green", "blue"]


def test_for_each_loop_over_string():
    _, output = execute(
        "for each char in \"abc\" {\n"
        "  say char\n"
        "}\n"
    )
    assert output == ["a", "b", "c"]


# ---------------------------------------------------------------------------
# `repeat N times` Loops
# ---------------------------------------------------------------------------


def test_repeat_loop_basic_execution():
    _, output = execute(
        "set count to 0\n"
        "repeat 3 times {\n"
        "  set count to count + 1\n"
        "  say count\n"
        "}\n"
    )
    assert output == ["1", "2", "3"]


def test_repeat_loop_zero_and_negative_counts():
    _, output = execute(
        "repeat 0 times { say \"never\" }\n"
        "repeat -5 times { say \"never\" }\n"
        "say \"done\"\n"
    )
    assert output == ["done"]


def test_repeat_loop_with_break_and_continue():
    _, output = execute(
        "set i to 0\n"
        "repeat 5 times {\n"
        "  set i to i + 1\n"
        "  if i == 2 { continue }\n"
        "  if i == 4 { break }\n"
        "  say i\n"
        "}\n"
    )
    assert output == ["1", "3"]


def test_repeat_loop_with_return_inside_function():
    _, output = execute(
        "function early_exit {\n"
        "  set k to 0\n"
        "  repeat 10 times {\n"
        "    set k to k + 1\n"
        "    if k == 3 { return k }\n"
        "  }\n"
        "}\n"
        "say early_exit()\n"
    )
    assert output == ["3"]


# ---------------------------------------------------------------------------
# Indexing & 0.4 Interactions with Functions
# ---------------------------------------------------------------------------


def test_indexing_return_values_and_function_lists():
    _, output = execute(
        "function get_items { return [100, 200, 300] }\n"
        "say get_items()[1]\n"
        "function make_fn taking x {\n"
        "  function inner { return x * 10 }\n"
        "  return inner\n"
        "}\n"
        "set funcs to [make_fn(1), make_fn(2)]\n"
        "say funcs[0]()\n"
        "say funcs[1]()\n"
    )
    assert output == ["200", "10", "20"]


# ---------------------------------------------------------------------------
# Error Diagnostics & Edge Cases
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("source", "match_msg"),
    [
        ("set items to [1, 2]\nsay items[5]\n", "List index out of range: 5"),
        ("set items to [1, 2]\nsay items[-1]\n", "List index out of range: -1"),
        ("set items to [1, 2]\nset items[5] to 10\n", "List index out of range: 5"),
        ("set word to \"hi\"\nsay word[5]\n", "String index out of range: 5"),
        ("set word to \"hi\"\nsay word[-1]\n", "String index out of range: -1"),
        ("set word to \"hi\"\nset word[0] to \"x\"\n", "Cannot assign to string index"),
        ("set items to [1, 2]\nsay items[\"a\"]\n", "List index must be an integer"),
        ("set items to [1, 2]\nsay items[1.5]\n", "List index must be an integer"),
        ("set items to [1, 2]\nsay items[true]\n", "List index must be an integer"),
        ("set items to [1, 2]\nsay items[nothing]\n", "List index must be an integer"),
        ("set word to \"hi\"\nsay word[\"a\"]\n", "String index must be an integer"),
        ("set user to {\"a\": 1}\nsay user[\"b\"]\n", "Key not found: \"b\""),
        ("set user to {\"a\": 1}\nsay user[[1, 2]]\n", "Dictionary keys must be numbers"),
        ("set n to 42\nsay n[0]\n", "Cannot index number"),
        ("set b to true\nsay b[0]\n", "Cannot index boolean"),
        ("set x to nothing\nsay x[0]\n", "Cannot index nothing"),
        ("function f {}\nsay f[0]\n", "Cannot index function"),
        ("set n to 42\nset n[0] to 1\n", "Cannot assign to index of number"),
        ("repeat \"bad\" times { }\n", "Repeat count requires a number"),
    ],
)
def test_runtime_errors_with_source_locations(source, match_msg):
    with pytest.raises(RuntimeError, match=match_msg) as error:
        execute(source)
    assert error.value.line is not None
    assert error.value.column is not None


@pytest.mark.parametrize(
    ("source", "match_msg"),
    [
        ("repeat 5 { }\n", "Expected 'times' after repeat count"),
        ("repeat 5 times\n", "Expected '{' after repeat statement"),
        ("if x is at 10 { }\n", "Expected 'least' or 'most' after 'is at'"),
        ("if x is greater 10 { }\n", "Expected 'than' after 'is greater'"),
        ("if x is equal 10 { }\n", "Expected 'to' after 'is equal'"),
        ("set [1, 2] to 3\n", "Expected variable name or index target after 'set'"),
    ],
)
def test_parser_errors_with_source_locations(source, match_msg):
    with pytest.raises(ParserError, match=match_msg) as error:
        parse(source)
    assert error.value.line is not None
    assert error.value.column is not None
