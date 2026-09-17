"""Standard library functions for Clarity 0.5."""

import math
from pathlib import Path
import random as _random_module

from .errors import RuntimeError
from .runtime import ClarityDict, ClarityNativeFunction
from . import semantics


class FileSystem:
    """Pluggable filesystem interface for local execution or sandboxed playgrounds."""

    def read_text(self, path: str) -> str:
        p = Path(path)
        try:
            if not p.exists():
                raise RuntimeError(f"File not found: '{path}'")
            if p.is_dir():
                raise RuntimeError(f"Path is a directory: '{path}'")
            return p.read_text(encoding="utf-8")
        except UnicodeDecodeError as err:
            raise RuntimeError(f"Could not read file '{path}': invalid UTF-8 encoding ({err})")
        except OSError as err:
            raise RuntimeError(f"Could not read file '{path}': {err}")

    def write_text(self, path: str, content: str) -> None:
        p = Path(path)
        try:
            if p.is_dir():
                raise RuntimeError(f"Cannot write to file '{path}': path is a directory")
            if p.parent and not p.parent.exists():
                p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content, encoding="utf-8")
        except OSError as err:
            raise RuntimeError(f"Could not write to file '{path}': {err}")

    def exists(self, path: str) -> bool:
        try:
            return Path(path).exists()
        except OSError:
            return False


DEFAULT_FILESYSTEM = FileSystem()


def _length(value: object) -> int:
    if isinstance(value, (str, list, dict, ClarityDict)):
        return len(value)
    raise RuntimeError(f"Cannot get length of {semantics.type_name(value)}")


def _uppercase(text: object) -> str:
    if not isinstance(text, str):
        raise RuntimeError(f"uppercase() requires a string, got {semantics.type_name(text)}")
    return text.upper()


def _lowercase(text: object) -> str:
    if not isinstance(text, str):
        raise RuntimeError(f"lowercase() requires a string, got {semantics.type_name(text)}")
    return text.lower()


def _trim(text: object) -> str:
    if not isinstance(text, str):
        raise RuntimeError(f"trim() requires a string, got {semantics.type_name(text)}")
    return text.strip()


def _contains(collection: object, value: object) -> bool:
    if isinstance(collection, str):
        if not isinstance(value, str):
            raise RuntimeError(f"contains() on string requires string substring, got {semantics.type_name(value)}")
        return value in collection
    if isinstance(collection, list):
        return any(semantics.equal(item, value) for item in collection)
    if isinstance(collection, (dict, ClarityDict)):
        semantics.validate_dictionary_key(value)
        return value in collection
    raise RuntimeError(f"contains() requires a string, list, or dictionary, got {semantics.type_name(collection)}")


def _replace(text: object, old: object, new: object) -> str:
    if not isinstance(text, str):
        raise RuntimeError(f"replace() requires a string target, got {semantics.type_name(text)}")
    if not isinstance(old, str):
        raise RuntimeError(f"replace() requires a string pattern to replace, got {semantics.type_name(old)}")
    if not isinstance(new, str):
        raise RuntimeError(f"replace() requires a string replacement, got {semantics.type_name(new)}")
    return text.replace(old, new)


def _split(text: object, separator: object) -> list[str]:
    if not isinstance(text, str):
        raise RuntimeError(f"split() requires a string target, got {semantics.type_name(text)}")
    if not isinstance(separator, str):
        raise RuntimeError(f"split() requires a string separator, got {semantics.type_name(separator)}")
    if separator == "":
        raise RuntimeError("split() separator cannot be empty")
    return text.split(separator)


def _join(items: object, separator: object) -> str:
    if not isinstance(items, list):
        raise RuntimeError(f"join() requires a list of items, got {semantics.type_name(items)}")
    if not isinstance(separator, str):
        raise RuntimeError(f"join() requires a string separator, got {semantics.type_name(separator)}")
    return separator.join(semantics.stringify(item) for item in items)


def _reverse(collection: object) -> object:
    if isinstance(collection, list):
        return list(reversed(collection))
    if isinstance(collection, str):
        return collection[::-1]
    raise RuntimeError(f"reverse() requires a list or string, got {semantics.type_name(collection)}")


def _sort(collection: object) -> list[object]:
    if not isinstance(collection, list):
        raise RuntimeError(f"sort() requires a list, got {semantics.type_name(collection)}")
    if not collection:
        return []
    if all(semantics.is_number(x) for x in collection):
        return sorted(collection)
    if all(isinstance(x, str) for x in collection):
        return sorted(collection)
    raise RuntimeError("sort() requires a list of all numbers or all strings")


def _abs(number: object) -> int | float:
    val = semantics.require_number(number, "abs()")
    return abs(val)


def _floor(number: object) -> int:
    val = semantics.require_number(number, "floor()")
    return math.floor(val)


def _ceil(number: object) -> int:
    val = semantics.require_number(number, "ceil()")
    return math.ceil(val)


def _round(number: object, digits: object = None) -> int | float:
    val = semantics.require_number(number, "round()")
    if digits is None:
        return round(val)
    if not semantics.is_number(digits) or not (isinstance(digits, int) or digits.is_integer()):
        raise RuntimeError(f"round() digits must be an integer, got {semantics.type_name(digits)}")
    return round(val, int(digits))


def _min(*args: object) -> object:
    if len(args) == 0:
        raise RuntimeError("min() expects at least 1 argument")
    if len(args) == 1:
        single = args[0]
        if isinstance(single, list):
            if not single:
                raise RuntimeError("min() on empty list")
            if all(semantics.is_number(x) for x in single):
                return min(single)
            if all(isinstance(x, str) for x in single):
                return min(single)
            raise RuntimeError("min() requires a list of all numbers or all strings")
        if semantics.is_number(single) or isinstance(single, str):
            return single
        raise RuntimeError(f"min() requires numbers or strings, got {semantics.type_name(single)}")
    if all(semantics.is_number(x) for x in args):
        return min(args)
    if all(isinstance(x, str) for x in args):
        return min(args)
    raise RuntimeError("min() requires all numbers or all strings")


def _max(*args: object) -> object:
    if len(args) == 0:
        raise RuntimeError("max() expects at least 1 argument")
    if len(args) == 1:
        single = args[0]
        if isinstance(single, list):
            if not single:
                raise RuntimeError("max() on empty list")
            if all(semantics.is_number(x) for x in single):
                return max(single)
            if all(isinstance(x, str) for x in single):
                return max(single)
            raise RuntimeError("max() requires a list of all numbers or all strings")
        if semantics.is_number(single) or isinstance(single, str):
            return single
        raise RuntimeError(f"max() requires numbers or strings, got {semantics.type_name(single)}")
    if all(semantics.is_number(x) for x in args):
        return max(args)
    if all(isinstance(x, str) for x in args):
        return max(args)
    raise RuntimeError("max() requires all numbers or all strings")


def _sqrt(number: object) -> int | float:
    val = semantics.require_number(number, "sqrt()")
    if val < 0:
        raise RuntimeError("sqrt() requires a non-negative number")
    if isinstance(val, int):
        root = math.isqrt(val)
        if root * root == val:
            return root
    return math.sqrt(val)


def _power(base: object, exponent: object) -> int | float:
    b = semantics.require_number(base, "power() base")
    e = semantics.require_number(exponent, "power() exponent")
    if b == 0 and e < 0:
        raise RuntimeError("Cannot raise zero to a negative power")
    if b < 0 and not (isinstance(e, int) or (isinstance(e, float) and e.is_integer())):
        raise RuntimeError("Cannot raise negative number to a non-integer power")
    try:
        res = b ** e
        if isinstance(res, complex):
            raise RuntimeError("Complex numbers are not supported")
        if isinstance(b, int) and isinstance(e, int) and e >= 0:
            return int(res)
        return res
    except OverflowError:
        raise RuntimeError("Result of power() is too large")


def _random(minimum: object, maximum: object, rand: _random_module.Random | None = None) -> int | float:
    min_val = semantics.require_number(minimum, "random() minimum")
    max_val = semantics.require_number(maximum, "random() maximum")
    if min_val > max_val:
        raise RuntimeError(f"random() minimum ({min_val}) cannot be greater than maximum ({max_val})")
    generator = rand or _random_module
    if isinstance(minimum, int) and isinstance(maximum, int):
        return generator.randint(minimum, maximum)
    return generator.uniform(min_val, max_val)


def _choose(items: object, rand: _random_module.Random | None = None) -> object:
    if not isinstance(items, (list, str)):
        raise RuntimeError(f"choose() requires a list or string, got {semantics.type_name(items)}")
    if len(items) == 0:
        raise RuntimeError("choose() requires a non-empty list or string")
    generator = rand or _random_module
    return generator.choice(items)


def create_standard_library(
    filesystem: FileSystem | None = None,
    rand: _random_module.Random | None = None,
) -> dict[str, ClarityNativeFunction]:
    """Create a dictionary of standard-library functions configured with optional providers."""
    fs = filesystem or DEFAULT_FILESYSTEM

    def read_file(path: object) -> str:
        if not isinstance(path, str):
            raise RuntimeError(f"read_file() requires a string path, got {semantics.type_name(path)}")
        return fs.read_text(path)

    def write_file(path: object, content: object) -> None:
        if not isinstance(path, str):
            raise RuntimeError(f"write_file() requires a string path, got {semantics.type_name(path)}")
        if not isinstance(content, str):
            raise RuntimeError(f"write_file() requires string content, got {semantics.type_name(content)}")
        fs.write_text(path, content)
        return None

    def file_exists(path: object) -> bool:
        if not isinstance(path, str):
            raise RuntimeError(f"file_exists() requires a string path, got {semantics.type_name(path)}")
        return fs.exists(path)

    def random_func(minimum: object, maximum: object) -> int | float:
        return _random(minimum, maximum, rand=rand)

    def choose_func(items: object) -> object:
        return _choose(items, rand=rand)

    return {
        # Text & Collections
        "length": ClarityNativeFunction("length", _length, min_arity=1, max_arity=1, doc="Returns length of string, list, or dictionary."),
        "uppercase": ClarityNativeFunction("uppercase", _uppercase, min_arity=1, max_arity=1, doc="Converts string to uppercase."),
        "lowercase": ClarityNativeFunction("lowercase", _lowercase, min_arity=1, max_arity=1, doc="Converts string to lowercase."),
        "trim": ClarityNativeFunction("trim", _trim, min_arity=1, max_arity=1, doc="Trims leading and trailing whitespace from string."),
        "contains": ClarityNativeFunction("contains", _contains, min_arity=2, max_arity=2, doc="Checks if string substring, list item, or dictionary key exists."),
        "replace": ClarityNativeFunction("replace", _replace, min_arity=3, max_arity=3, doc="Replaces occurrences of old substring with new substring."),
        "split": ClarityNativeFunction("split", _split, min_arity=2, max_arity=2, doc="Splits string by separator into a list of strings."),
        "join": ClarityNativeFunction("join", _join, min_arity=2, max_arity=2, doc="Joins list of items with separator into a string."),
        "reverse": ClarityNativeFunction("reverse", _reverse, min_arity=1, max_arity=1, doc="Returns reversed copy of list or string."),
        "sort": ClarityNativeFunction("sort", _sort, min_arity=1, max_arity=1, doc="Returns sorted copy of list of numbers or strings."),

        # Math
        "abs": ClarityNativeFunction("abs", _abs, min_arity=1, max_arity=1, doc="Returns absolute value of number."),
        "floor": ClarityNativeFunction("floor", _floor, min_arity=1, max_arity=1, doc="Returns floor of number as integer."),
        "ceil": ClarityNativeFunction("ceil", _ceil, min_arity=1, max_arity=1, doc="Returns ceiling of number as integer."),
        "round": ClarityNativeFunction("round", _round, min_arity=1, max_arity=2, doc="Rounds number to nearest integer or specified decimal places."),
        "min": ClarityNativeFunction("min", _min, min_arity=1, max_arity=-1, doc="Returns minimum value among arguments or list elements."),
        "max": ClarityNativeFunction("max", _max, min_arity=1, max_arity=-1, doc="Returns maximum value among arguments or list elements."),
        "sqrt": ClarityNativeFunction("sqrt", _sqrt, min_arity=1, max_arity=1, doc="Returns square root of non-negative number."),
        "power": ClarityNativeFunction("power", _power, min_arity=2, max_arity=2, doc="Returns base raised to exponent."),

        # Random
        "random": ClarityNativeFunction("random", random_func, min_arity=2, max_arity=2, doc="Returns random integer (if integer bounds) or float between min and max inclusive."),
        "choose": ClarityNativeFunction("choose", choose_func, min_arity=1, max_arity=1, doc="Returns randomly chosen element from list or string."),

        # Files
        "read_file": ClarityNativeFunction("read_file", read_file, min_arity=1, max_arity=1, doc="Reads text file with UTF-8 encoding."),
        "write_file": ClarityNativeFunction("write_file", write_file, min_arity=2, max_arity=2, doc="Writes text content to file with UTF-8 encoding."),
        "file_exists": ClarityNativeFunction("file_exists", file_exists, min_arity=1, max_arity=1, doc="Checks if file or path exists."),
    }


def get_standard_library() -> dict[str, ClarityNativeFunction]:
    """Get the standard library with default filesystem and random provider."""
    return create_standard_library()
