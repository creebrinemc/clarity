"""Comprehensive tests for Clarity 0.5 standard library."""

import pytest
from pathlib import Path

from clarity.cli import run_source
from clarity.errors import RuntimeError
from clarity.evaluator import Evaluator
from clarity.lexer import Lexer
from clarity.parser import Parser


def execute(source: str) -> list[str]:
    output: list[str] = []
    evaluator = Evaluator(output=output.append)
    evaluator.evaluate(Parser(Lexer(source).tokenize()).parse())
    return output


def evaluate_expression(source: str) -> object:
    evaluator = Evaluator()
    return evaluator.evaluate(Parser(Lexer(source).tokenize()).parse())


# ==========================================
# TEXT TESTS
# ==========================================

def test_length_text():
    assert execute('say length("hello")') == ["5"]
    assert execute('say length("")') == ["0"]
    assert execute('say length("café")') == ["4"]
    assert execute('say length("🚀🌟")') == ["2"]


def test_uppercase():
    assert execute('say uppercase("hello world")') == ["HELLO WORLD"]
    assert execute('say uppercase("café")') == ["CAFÉ"]
    assert execute('say uppercase("123 ABC")') == ["123 ABC"]


def test_lowercase():
    assert execute('say lowercase("HELLO WORLD")') == ["hello world"]
    assert execute('say lowercase("CAFÉ")') == ["café"]


def test_trim():
    assert execute('say trim("  hello  ")') == ["hello"]
    assert execute(r'say trim("\t\n  spaced  \n\t")') == ["spaced"]
    assert execute('say trim("no_trim")') == ["no_trim"]
    assert execute('say trim("")') == [""]


def test_contains_text():
    assert execute('say contains("hello world", "world")') == ["true"]
    assert execute('say contains("hello world", "earth")') == ["false"]
    assert execute('say contains("hello", "")') == ["true"]


def test_replace():
    assert execute('say replace("hello world", "world", "clarity")') == ["hello clarity"]
    assert execute('say replace("banana", "a", "o")') == ["bonono"]
    assert execute('say replace("banana", "x", "y")') == ["banana"]


def test_split():
    assert execute('say split("a,b,c", ",")') == ['["a", "b", "c"]']
    assert execute('say split("hello", " ")') == ['["hello"]']
    assert execute('say split("one--two--three", "--")') == ['["one", "two", "three"]']


def test_join():
    assert execute('say join(["a", "b", "c"], ", ")') == ["a, b, c"]
    assert execute('say join([1, 2, 3], "-")') == ["1-2-3"]
    assert execute('say join([], ", ")') == [""]
    assert execute('say join(["single"], ", ")') == ["single"]
    assert execute('say join([true, false, nothing], ":")') == ["true:false:nothing"]


def test_text_invalid_types():
    with pytest.raises(RuntimeError, match="uppercase\\(\\) requires a string"):
        execute("uppercase(123)")
    with pytest.raises(RuntimeError, match="lowercase\\(\\) requires a string"):
        execute("lowercase(true)")
    with pytest.raises(RuntimeError, match="trim\\(\\) requires a string"):
        execute("trim([1, 2])")
    with pytest.raises(RuntimeError, match="contains\\(\\) on string requires string substring"):
        execute('contains("abc", 123)')
    with pytest.raises(RuntimeError, match="replace\\(\\) requires a string"):
        execute('replace(123, "a", "b")')
    with pytest.raises(RuntimeError, match="split\\(\\) requires a string"):
        execute('split(123, ",")')
    with pytest.raises(RuntimeError, match="split\\(\\) separator cannot be empty"):
        execute('split("abc", "")')
    with pytest.raises(RuntimeError, match="join\\(\\) requires a list of items"):
        execute('join("not a list", ",")')
    with pytest.raises(RuntimeError, match="join\\(\\) requires a string separator"):
        execute('join(["a", "b"], 123)')


# ==========================================
# COLLECTIONS TESTS
# ==========================================

def test_length_collections():
    assert execute("say length([1, 2, 3, 4])") == ["4"]
    assert execute("say length([])") == ["0"]
    assert execute('say length({ name: "Clarity", version: 5 })') == ["2"]
    assert execute("say length({})") == ["0"]


def test_length_invalid_type():
    with pytest.raises(RuntimeError, match="Cannot get length of number"):
        execute("length(123)")
    with pytest.raises(RuntimeError, match="Cannot get length of boolean"):
        execute("length(true)")
    with pytest.raises(RuntimeError, match="Cannot get length of nothing"):
        execute("length(nothing)")


def test_contains_collections():
    assert execute('say contains([1, 2, 3], 2)') == ["true"]
    assert execute('say contains([1, 2, 3], 4)') == ["false"]
    assert execute('say contains(["apple", "banana"], "apple")') == ["true"]
    # Distinct types: 1 != True in Clarity
    assert execute('say contains([true, false], 1)') == ["false"]
    assert execute('say contains([1, 2], true)') == ["false"]
    # Dictionary contains
    assert execute('say contains({ name: "Creebrine", age: 14 }, "name")') == ["true"]
    assert execute('say contains({ name: "Creebrine", age: 14 }, "score")') == ["false"]


def test_reverse():
    # Reverse list without mutating original
    code = """
    set original to [1, 2, 3]
    set rev to reverse(original)
    say rev
    say original
    """
    assert execute(code) == ["[3, 2, 1]", "[1, 2, 3]"]

    # Reverse string
    assert execute('say reverse("clarity")') == ["ytiralc"]
    assert execute('say reverse("")') == [""]


def test_reverse_invalid_type():
    with pytest.raises(RuntimeError, match="reverse\\(\\) requires a list or string"):
        execute("reverse(123)")


def test_sort():
    # Sort numbers without mutating original
    code = """
    set numbers to [4, 1, 3, 2]
    set sorted_numbers to sort(numbers)
    say sorted_numbers
    say numbers
    """
    assert execute(code) == ["[1, 2, 3, 4]", "[4, 1, 3, 2]"]

    # Sort strings
    assert execute('say sort(["cherry", "apple", "banana"])') == ['["apple", "banana", "cherry"]']
    assert execute("say sort([])") == ["[]"]


def test_sort_mixed_types_error():
    with pytest.raises(RuntimeError, match="sort\\(\\) requires a list of all numbers or all strings"):
        execute('sort([1, "two", 3])')
    with pytest.raises(RuntimeError, match="sort\\(\\) requires a list of all numbers or all strings"):
        execute("sort([true, false])")
    with pytest.raises(RuntimeError, match="sort\\(\\) requires a list"):
        execute('sort("not a list")')


# ==========================================
# MATH TESTS
# ==========================================

def test_abs():
    assert execute("say abs(-5)") == ["5"]
    assert execute("say abs(5)") == ["5"]
    assert execute("say abs(-3.14)") == ["3.14"]
    assert execute("say abs(0)") == ["0"]


def test_floor():
    assert execute("say floor(3.7)") == ["3"]
    assert execute("say floor(-3.7)") == ["-4"]
    assert execute("say floor(5)") == ["5"]


def test_ceil():
    assert execute("say ceil(3.2)") == ["4"]
    assert execute("say ceil(-3.2)") == ["-3"]
    assert execute("say ceil(5)") == ["5"]


def test_round():
    assert execute("say round(3.2)") == ["3"]
    assert execute("say round(3.8)") == ["4"]
    assert execute("say round(3.14159, 2)") == ["3.14"]
    assert execute("say round(3.14159, 0)") == ["3.0"]


def test_min():
    assert execute("say min(1, 2, 3)") == ["1"]
    assert execute("say min(10, -5, 20)") == ["-5"]
    assert execute("say min([10, -5, 20])") == ["-5"]
    assert execute('say min("apple", "banana", "zebra")') == ["apple"]
    assert execute('say min(["cherry", "apple", "banana"])') == ["apple"]
    assert execute("say min(42)") == ["42"]


def test_max():
    assert execute("say max(1, 2, 3)") == ["3"]
    assert execute("say max(10, -5, 20)") == ["20"]
    assert execute("say max([10, -5, 20])") == ["20"]
    assert execute('say max("apple", "banana", "zebra")') == ["zebra"]
    assert execute('say max(["cherry", "apple", "banana"])') == ["cherry"]
    assert execute("say max(42)") == ["42"]


def test_min_max_errors():
    with pytest.raises(RuntimeError, match="min\\(\\) on empty list"):
        execute("min([])")
    with pytest.raises(RuntimeError, match="max\\(\\) on empty list"):
        execute("max([])")
    with pytest.raises(RuntimeError, match="min\\(\\) requires all numbers or all strings"):
        execute('min(1, "two")')
    with pytest.raises(RuntimeError, match="max\\(\\) requires all numbers or all strings"):
        execute('max(1, "two")')


def test_sqrt():
    assert execute("say sqrt(25)") == ["5"]
    assert execute("say sqrt(0)") == ["0"]
    assert execute("say sqrt(4)") == ["2"]
    assert execute("say sqrt(2)") == [str(2 ** 0.5)]


def test_sqrt_negative():
    with pytest.raises(RuntimeError, match="sqrt\\(\\) requires a non-negative number"):
        execute("sqrt(-1)")


def test_power():
    assert execute("say power(2, 3)") == ["8"]
    assert execute("say power(2, 8)") == ["256"]
    assert execute("say power(5, 0)") == ["1"]
    assert execute("say power(2, -1)") == ["0.5"]
    assert execute("say power(4, 0.5)") == ["2.0"]


def test_power_errors():
    with pytest.raises(RuntimeError, match="Cannot raise zero to a negative power"):
        execute("power(0, -1)")
    with pytest.raises(RuntimeError, match="Cannot raise negative number to a non-integer power"):
        execute("power(-4, 0.5)")


# ==========================================
# RANDOM TESTS
# ==========================================

def test_random_integer_bounds():
    code = """
    set val to random(10, 20)
    say val >= 10 and val <= 20
    """
    assert execute(code) == ["true"]


def test_random_float_bounds():
    code = """
    set val to random(1.0, 5.0)
    say val >= 1.0 and val <= 5.0
    """
    assert execute(code) == ["true"]


def test_random_invalid_range():
    with pytest.raises(RuntimeError, match="random\\(\\) minimum \\(20\\) cannot be greater than maximum \\(10\\)"):
        execute("random(20, 10)")


def test_choose():
    code = """
    set items to ["apple", "banana", "cherry"]
    set chosen to choose(items)
    say contains(items, chosen)
    """
    assert execute(code) == ["true"]

    str_code = """
    set s to "xyz"
    set ch to choose(s)
    say contains(s, ch)
    """
    assert execute(str_code) == ["true"]


def test_choose_empty():
    with pytest.raises(RuntimeError, match="choose\\(\\) requires a non-empty list or string"):
        execute("choose([])")
    with pytest.raises(RuntimeError, match="choose\\(\\) requires a non-empty list or string"):
        execute('choose("")')


# ==========================================
# FILES TESTS
# ==========================================

def test_files_write_read_exists(tmp_path: Path):
    file_path = str(tmp_path / "test.txt")
    code = f"""
    say file_exists("{file_path}")
    write_file("{file_path}", "Hello Clarity Files!")
    say file_exists("{file_path}")
    say read_file("{file_path}")
    """
    assert execute(code) == ["false", "true", "Hello Clarity Files!"]


def test_read_nonexistent_file(tmp_path: Path):
    nonexistent = str(tmp_path / "nonexistent.txt")
    with pytest.raises(RuntimeError, match=f"File not found: '{nonexistent}'"):
        execute(f'read_file("{nonexistent}")')


def test_read_directory(tmp_path: Path):
    dir_path = str(tmp_path)
    with pytest.raises(RuntimeError, match=f"Path is a directory: '{dir_path}'"):
        execute(f'read_file("{dir_path}")')


def test_write_file_directory_error(tmp_path: Path):
    dir_path = str(tmp_path)
    with pytest.raises(RuntimeError, match=f"Cannot write to file '{dir_path}': path is a directory"):
        execute(f'write_file("{dir_path}", "data")')


# ==========================================
# FIRST-CLASS FUNCTIONS & GENERAL INTERACTION
# ==========================================

def test_stdlib_first_class_values():
    code = """
    set op to uppercase
    say op
    say op("first class")

    function apply taking func and arg {
        return func(arg)
    }

    say apply(lowercase, "HELLO")
    say apply(sqrt, 100)
    """
    assert execute(code) == [
        "<function uppercase>",
        "FIRST CLASS",
        "hello",
        "10",
    ]


def test_stdlib_shadowing():
    code = """
    set sqrt to "not a function"
    say sqrt
    """
    assert execute(code) == ["not a function"]


def test_stdlib_closure_interaction():
    code = """
    function make_trimmer_and_uppercaser {
        function transform taking text {
            return uppercase(trim(text))
        }
        return transform
    }
    set transform to make_trimmer_and_uppercaser()
    say transform("   clarity lang   ")
    """
    assert execute(code) == ["CLARITY LANG"]


def test_stdlib_arity_errors():
    with pytest.raises(RuntimeError, match="Function 'length' expects 1 argument\\(s\\), got 0"):
        execute("length()")
    with pytest.raises(RuntimeError, match="Function 'length' expects 1 argument\\(s\\), got 2"):
        execute('length("a", "b")')
    with pytest.raises(RuntimeError, match="Function 'replace' expects 3 argument\\(s\\), got 2"):
        execute('replace("a", "b")')
    with pytest.raises(RuntimeError, match="Function 'round' expects between 1 and 2 argument\\(s\\), got 3"):
        execute("round(1, 2, 3)")


def test_stdlib_error_source_spans():
    code = """
    set x to 10
    say uppercase(x)
    """
    with pytest.raises(RuntimeError) as exc_info:
        execute(code)
    assert exc_info.value.line == 3
    assert exc_info.value.column == 9


# ==========================================
# ADVANCED & EDGE CASE TESTS
# ==========================================

def test_sort_numbers_with_floats_and_negatives():
    code = """
    set items to [3.5, -2, 0, 10, -2.5]
    say sort(items)
    """
    assert execute(code) == ["[-2.5, -2, 0, 3.5, 10]"]


def test_power_negative_base_integer_exponent():
    assert execute("say power(-2, 3)") == ["-8"]
    assert execute("say power(-2, 4)") == ["16"]


def test_files_unicode_and_overwrite(tmp_path: Path):
    file_path = str(tmp_path / "unicode.txt")
    code = f"""
    write_file("{file_path}", "🌟 Hello Clarity 0.5 — Türkçe: Şeker 🍬")
    say read_file("{file_path}")
    write_file("{file_path}", "Overwritten content")
    say read_file("{file_path}")
    """
    assert execute(code) == [
        "🌟 Hello Clarity 0.5 — Türkçe: Şeker 🍬",
        "Overwritten content",
    ]


def test_custom_filesystem_and_random_provider():
    import random
    from clarity.stdlib import FileSystem, create_standard_library

    class MemoryFileSystem(FileSystem):
        def __init__(self):
            self.store = {}
        def read_text(self, path: str) -> str:
            if path in self.store:
                return self.store[path]
            raise RuntimeError(f"File not found: '{path}'")
        def write_text(self, path: str, content: str) -> None:
            self.store[path] = content
        def exists(self, path: str) -> bool:
            return path in self.store

    mem_fs = MemoryFileSystem()
    seeded_rand = random.Random(42)
    lib = create_standard_library(filesystem=mem_fs, rand=seeded_rand)

    evaluator = Evaluator()
    evaluator.environment.values.update(lib)
    outputs = []
    evaluator.output = outputs.append

    evaluator.evaluate(Parser(Lexer('write_file("virtual.txt", "Virtual FS content")').tokenize()).parse())
    evaluator.evaluate(Parser(Lexer('say read_file("virtual.txt")').tokenize()).parse())
    evaluator.evaluate(Parser(Lexer('say random(1, 100)').tokenize()).parse())

    assert outputs[0] == "Virtual FS content"
    assert outputs[1] == "82"  # Exact randint(1, 100) with seed 42 in Python 3.14


def test_nested_standard_library_calls():
    code = """
    say sqrt(power(2, 6))
    say round(sqrt(2), 3)
    say uppercase(trim(replace("  hello world  ", "world", "clarity")))
    say join(sort(["zebra", "apple", "mango"]), " -> ")
    """
    assert execute(code) == [
        "8",
        "1.414",
        "HELLO CLARITY",
        "apple -> mango -> zebra",
    ]


def test_stdlib_in_loops_and_conditionals():
    code = """
    set words to ["  one  ", "  two  ", "  three  "]
    set cleaned to []
    for each word in words {
        push uppercase(trim(word)) to cleaned
    }
    say cleaned
    """
    assert execute(code) == ['["ONE", "TWO", "THREE"]']


def test_contains_with_nothing_and_special_keys():
    code = """
    set items to [1, nothing, "text", false]
    say contains(items, nothing)
    say contains(items, true)

    set d to { nothing: "val" }
    say contains(d, nothing)
    """
    assert execute(code) == ["true", "false", "true"]
