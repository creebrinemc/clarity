import pytest

from clarity.cli import run_source
from clarity.environment import Environment
from clarity.evaluator import Evaluator
from clarity.errors import RuntimeError
from clarity.lexer import Lexer
from clarity.parser import Parser


def execute(source):
    output = []
    evaluator = Evaluator(output=output.append)
    evaluator.evaluate(Parser(Lexer(source).tokenize()).parse())
    return evaluator.environment, output


def test_variables_arithmetic_and_precedence():
    environment, _ = execute("set score to 2 + 3 * 4\n")
    assert environment.get("score") == 14


def test_comparisons_booleans_and_strings():
    environment, _ = execute('set message to "Hi " + "there"\nset valid to not false and 3 >= 2\n')
    assert environment.get("message") == "Hi there"
    assert environment.get("valid") is True


def test_lists_dictionaries_push_and_pop():
    environment, _ = execute('set items to ["Sword"]\npush "Potion" to items\npop from items\nset user to {"name": "Creebrine"}\n')
    assert environment.get("items") == ["Sword"]
    assert environment.get("user") == {"name": "Creebrine"}


def test_say_and_complete_program_integration():
    environment, output = execute('set first to 10\nset second to 5\nset result to (first + second) * 2\nsay result\n')
    assert environment.get("result") == 30
    assert output == ["30"]


def test_environment_is_scope_ready():
    parent = Environment(); parent.define("value", 1)
    child = Environment(parent)
    child.set("value", 2)
    assert parent.get("value") == 2


def test_environment_assigns_nearest_parent_or_defines_locally():
    parent = Environment()
    parent.define("parent_value", 1)
    child = Environment(parent)
    child.assign("parent_value", 2)
    child.assign("local_value", 3)
    assert parent.get("parent_value") == 2
    assert child.get("local_value") == 3
    with pytest.raises(RuntimeError, match="Unknown variable: local_value"):
        parent.get("local_value")


def test_reassignment_updates_existing_binding():
    environment, _ = execute("set score to 100\nset score to 200\n")
    assert environment.get("score") == 200


def test_boolean_semantics_and_string_conversion():
    _, output = execute(
        'say not nothing\nsay not 0\nsay true and 5\nsay nothing or "yes"\nsay ["Sword", true]\n'
    )
    assert output == ["true", "false", "true", "true", '["Sword", true]']


def test_nested_values_and_multiline_program_with_comments():
    environment, output = execute(
        "# setup\n\nset values to [{\"name\": \"Creebrine\", \"items\": []}]\n\nsay values\n"
    )
    assert environment.get("values") == [{"name": "Creebrine", "items": []}]
    assert output == ['[{"name": "Creebrine", "items": []}]']


@pytest.mark.parametrize(
    ("source", "message"),
    [
        ("say unknown\n", "Unknown variable"),
        ("say 1 / 0\n", "Cannot divide by zero"),
        ('say "a" - 1\n', "requires a number"),
        ("say 1 > true\n", "requires two numbers or two strings"),
        ("set value to 1\npush 2 to value\n", "not a list"),
        ("set value to 1\npop from value\n", "not a list"),
        ("set value to []\npop from value\n", "list is empty"),
    ],
)
def test_runtime_errors_are_clarity_errors_with_source_locations(source, message):
    with pytest.raises(RuntimeError, match=message) as error:
        execute(source)
    assert error.value.line is not None
    assert error.value.column is not None


def test_execute_block_updates_parent_or_defines_local_without_leaking():
    evaluator = Evaluator()
    evaluator.environment.define("outer", 1)
    block = Parser(Lexer("set outer to 2\nset local to 3\n").tokenize()).parse()
    evaluator.execute_block(block.statements)
    assert evaluator.environment.get("outer") == 2
    with pytest.raises(RuntimeError, match="Unknown variable: local"):
        evaluator.environment.get("local")
