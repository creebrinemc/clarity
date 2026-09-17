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
# Declarations
# ---------------------------------------------------------------------------


def test_zero_parameter_function_declaration():
    program = parse("function greet { say \"Hello\" }\n")
    decl = program.statements[0]
    assert isinstance(decl, ast.FunctionDeclarationNode)
    assert decl.name == "greet"
    assert decl.parameters == []
    assert len(decl.body.statements) == 1


def test_one_parameter_function_declaration():
    program = parse("function greet taking name { say \"Hello, \" + name }\n")
    decl = program.statements[0]
    assert isinstance(decl, ast.FunctionDeclarationNode)
    assert decl.name == "greet"
    assert len(decl.parameters) == 1
    assert decl.parameters[0].name == "name"


def test_multiple_parameters_declaration():
    program = parse("function add taking a and b and c { return a + b + c }\n")
    decl = program.statements[0]
    assert isinstance(decl, ast.FunctionDeclarationNode)
    assert decl.name == "add"
    assert [p.name for p in decl.parameters] == ["a", "b", "c"]


def test_nested_function_declarations():
    _, output = execute(
        "function outer {\n"
        "  function inner {\n"
        "    return \"nested\"\n"
        "  }\n"
        "  return inner()\n"
        "}\n"
        "say outer()\n"
    )
    assert output == ["nested"]


def test_duplicate_parameter_names_raise_parser_error():
    with pytest.raises(ParserError, match="Duplicate parameter name: item") as error:
        parse("function process taking item and item { }\n")
    assert error.value.line == 1
    assert error.value.column is not None


# ---------------------------------------------------------------------------
# Calls
# ---------------------------------------------------------------------------


def test_zero_argument_call():
    _, output = execute(
        "function get_greeting {\n"
        "  return \"hi\"\n"
        "}\n"
        "say get_greeting()\n"
    )
    assert output == ["hi"]


def test_one_argument_call():
    _, output = execute(
        "function square taking n {\n"
        "  return n * n\n"
        "}\n"
        "say square(6)\n"
    )
    assert output == ["36"]


def test_multiple_arguments_call():
    _, output = execute(
        "function sub taking a and b {\n"
        "  return a - b\n"
        "}\n"
        "say sub(10, 4)\n"
    )
    assert output == ["6"]


def test_calls_as_expressions_and_in_arithmetic():
    _, output = execute(
        "function double taking n { return n * 2 }\n"
        "set result to double(3) + double(4) * 2\n"
        "say result\n"
    )
    assert output == ["22"]


def test_standalone_function_calls():
    _, output = execute(
        "function log_msg taking msg {\n"
        "  say msg\n"
        "}\n"
        "log_msg(\"first\")\n"
        "log_msg(\"second\")\n"
    )
    assert output == ["first", "second"]


def test_chained_function_calls():
    _, output = execute(
        "function make_fn {\n"
        "  function nested {\n"
        "    return \"chained result\"\n"
        "  }\n"
        "  return nested\n"
        "}\n"
        "say make_fn()()\n"
    )
    assert output == ["chained result"]


# ---------------------------------------------------------------------------
# Returns
# ---------------------------------------------------------------------------


def test_return_expression():
    _, output = execute(
        "function add taking a and b { return a + b }\n"
        "say add(10, 20)\n"
    )
    assert output == ["30"]


def test_bare_return_produces_nothing():
    _, output = execute(
        "function stop_early {\n"
        "  return\n"
        "  say \"unreachable\"\n"
        "}\n"
        "say stop_early()\n"
    )
    assert output == ["nothing"]


def test_implicit_return_produces_nothing():
    _, output = execute(
        "function do_work {\n"
        "  set x to 42\n"
        "}\n"
        "say do_work()\n"
    )
    assert output == ["nothing"]


def test_early_return_skips_subsequent_statements():
    _, output = execute(
        "function check taking x {\n"
        "  if x > 0 {\n"
        "    return \"positive\"\n"
        "  }\n"
        "  say \"not positive\"\n"
        "  return \"non-positive\"\n"
        "}\n"
        "say check(5)\n"
        "say check(-1)\n"
    )
    assert output == ["positive", "not positive", "non-positive"]


def test_return_from_inside_loop():
    _, output = execute(
        "function find_first_even taking items {\n"
        "  for item in items {\n"
        "    if item % 2 == 0 {\n"
        "      return item\n"
        "    }\n"
        "  }\n"
        "  return nothing\n"
        "}\n"
        "say find_first_even([1, 3, 4, 7])\n"
        "say find_first_even([1, 3, 5])\n"
    )
    assert output == ["4", "nothing"]


def test_return_outside_function_raises_runtime_error():
    with pytest.raises(RuntimeError, match="'return' can only be used inside a function") as error:
        execute("return 10\n")
    assert error.value.line == 1
    assert error.value.column is not None


# ---------------------------------------------------------------------------
# Scope
# ---------------------------------------------------------------------------


def test_function_local_variables_do_not_leak():
    environment, _ = execute(
        "function compute {\n"
        "  set local_var to 99\n"
        "  return local_var\n"
        "}\n"
        "compute()\n"
    )
    with pytest.raises(RuntimeError, match="Unknown variable: local_var"):
        environment.get("local_var")


def test_parameters_are_local_and_do_not_leak():
    environment, _ = execute(
        "function greet taking name {\n"
        "  return \"Hello, \" + name\n"
        "}\n"
        "greet(\"Alice\")\n"
    )
    with pytest.raises(RuntimeError, match="Unknown variable: name"):
        environment.get("name")


def test_global_reads_from_function():
    _, output = execute(
        "set global_title to \"Clarity\"\n"
        "function show_title {\n"
        "  say global_title\n"
        "}\n"
        "show_title()\n"
    )
    assert output == ["Clarity"]


def test_nearest_binding_set_updates_outer_variable():
    environment, _ = execute(
        "set counter to 0\n"
        "function increment {\n"
        "  set counter to counter + 1\n"
        "}\n"
        "increment()\n"
        "increment()\n"
    )
    assert environment.get("counter") == 2


def test_nested_lexical_scopes_inside_function():
    _, output = execute(
        "function test_scopes {\n"
        "  set a to 1\n"
        "  if true {\n"
        "    set a to 2\n"
        "    set b to 3\n"
        "  }\n"
        "  say a\n"
        "}\n"
        "test_scopes()\n"
    )
    assert output == ["2"]


# ---------------------------------------------------------------------------
# Closures
# ---------------------------------------------------------------------------


def test_closure_captures_lexical_value():
    _, output = execute(
        "function make_adder taking x {\n"
        "  function add taking y {\n"
        "    return x + y\n"
        "  }\n"
        "  return add\n"
        "}\n"
        "set add5 to make_adder(5)\n"
        "say add5(10)\n"
        "say add5(20)\n"
    )
    assert output == ["15", "25"]


def test_closure_mutable_state():
    _, output = execute(
        "function make_counter {\n"
        "  set count to 0\n"
        "  function increment {\n"
        "    set count to count + 1\n"
        "    return count\n"
        "  }\n"
        "  return increment\n"
        "}\n"
        "set counter to make_counter()\n"
        "say counter()\n"
        "say counter()\n"
        "say counter()\n"
    )
    assert output == ["1", "2", "3"]


def test_independent_closure_instances():
    _, output = execute(
        "function make_counter {\n"
        "  set count to 0\n"
        "  function increment {\n"
        "    set count to count + 1\n"
        "    return count\n"
        "  }\n"
        "  return increment\n"
        "}\n"
        "set c1 to make_counter()\n"
        "set c2 to make_counter()\n"
        "say c1()\n"
        "say c1()\n"
        "say c2()\n"
        "say c1()\n"
        "say c2()\n"
    )
    assert output == ["1", "2", "1", "3", "2"]


# ---------------------------------------------------------------------------
# Recursion
# ---------------------------------------------------------------------------


def test_direct_recursion_factorial():
    _, output = execute(
        "function factorial taking n {\n"
        "  if n <= 1 {\n"
        "    return 1\n"
        "  }\n"
        "  return n * factorial(n - 1)\n"
        "}\n"
        "say factorial(5)\n"
        "say factorial(0)\n"
    )
    assert output == ["120", "1"]


def test_mutual_recursion():
    _, output = execute(
        "function is_even taking n {\n"
        "  if n == 0 { return true }\n"
        "  return is_odd(n - 1)\n"
        "}\n"
        "function is_odd taking n {\n"
        "  if n == 0 { return false }\n"
        "  return is_even(n - 1)\n"
        "}\n"
        "say is_even(4)\n"
        "say is_odd(4)\n"
        "say is_even(3)\n"
        "say is_odd(3)\n"
    )
    assert output == ["true", "false", "false", "true"]


# ---------------------------------------------------------------------------
# First-Class Functions
# ---------------------------------------------------------------------------


def test_assigning_and_calling_through_variable():
    _, output = execute(
        "function greet taking name { return \"Hello, \" + name }\n"
        "set f to greet\n"
        "say f(\"Creebrine\")\n"
    )
    assert output == ["Hello, Creebrine"]


def test_passing_function_as_argument():
    _, output = execute(
        "function apply taking fn and value {\n"
        "  return fn(value)\n"
        "}\n"
        "function double taking x { return x * 2 }\n"
        "function triple taking x { return x * 3 }\n"
        "say apply(double, 5)\n"
        "say apply(triple, 5)\n"
    )
    assert output == ["10", "15"]


def test_storing_functions_in_list_and_dictionary():
    _, output = execute(
        "function add taking a and b { return a + b }\n"
        "function mul taking a and b { return a * b }\n"
        "set funcs to [add, mul]\n"
        "set ops to {\"addition\": add, \"multiplication\": mul}\n"
        "say funcs\n"
        "say ops\n"
    )
    assert output == [
        "[<function add>, <function mul>]",
        '{"addition": <function add>, "multiplication": <function mul>}',
    ]


def test_stringifying_function():
    _, output = execute(
        "function my_function { }\n"
        "say my_function\n"
    )
    assert output == ["<function my_function>"]


# ---------------------------------------------------------------------------
# Argument Errors
# ---------------------------------------------------------------------------


def test_too_few_arguments_raises_runtime_error():
    with pytest.raises(RuntimeError, match="Function 'add' expects 2 argument\\(s\\), got 1") as error:
        execute("function add taking a and b { return a + b }\nadd(10)\n")
    assert error.value.line == 2
    assert error.value.column is not None


def test_too_many_arguments_raises_runtime_error():
    with pytest.raises(RuntimeError, match="Function 'add' expects 2 argument\\(s\\), got 3") as error:
        execute("function add taking a and b { return a + b }\nadd(1, 2, 3)\n")
    assert error.value.line == 2
    assert error.value.column is not None


def test_calling_non_function_raises_runtime_error():
    with pytest.raises(RuntimeError, match="Can only call functions") as error:
        execute("set not_a_func to 42\nnot_a_func()\n")
    assert error.value.line == 2
    assert error.value.column is not None


# ---------------------------------------------------------------------------
# Control-Flow Boundaries
# ---------------------------------------------------------------------------


def test_break_inside_function_called_from_loop_raises_runtime_error():
    with pytest.raises(RuntimeError, match="'break' can only be used inside a loop") as error:
        execute(
            "function escape {\n"
            "  break\n"
            "}\n"
            "while true {\n"
            "  escape()\n"
            "}\n"
        )
    assert error.value.line == 2
    assert error.value.column is not None


def test_continue_inside_function_called_from_loop_raises_runtime_error():
    with pytest.raises(RuntimeError, match="'continue' can only be used inside a loop") as error:
        execute(
            "function skip {\n"
            "  continue\n"
            "}\n"
            "while true {\n"
            "  skip()\n"
            "}\n"
        )
    assert error.value.line == 2
    assert error.value.column is not None


def test_function_internal_loop_break_and_continue_does_not_affect_caller():
    _, output = execute(
        "function loop_helper {\n"
        "  set k to 0\n"
        "  while true {\n"
        "    set k to k + 1\n"
        "    if k == 2 { continue }\n"
        "    if k == 3 { break }\n"
        "  }\n"
        "  return k\n"
        "}\n"
        "set outer to 0\n"
        "while outer < 2 {\n"
        "  set outer to outer + 1\n"
        "  say loop_helper()\n"
        "  say outer\n"
        "}\n"
    )
    assert output == ["3", "1", "3", "2"]


def test_return_from_nested_loop_inside_function_resets_loop_depth():
    _, output = execute(
        "function search {\n"
        "  while true {\n"
        "    while true {\n"
        "      return \"found\"\n"
        "    }\n"
        "  }\n"
        "}\n"
        "say search()\n"
    )
    assert output == ["found"]
