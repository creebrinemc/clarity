"""Explicit runtime rules for the currently supported Clarity values."""

from .errors import RuntimeError
from .runtime import ClarityFunction


def is_number(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def require_number(value: object, operation: str) -> int | float:
    if not is_number(value):
        raise RuntimeError(f"{operation} requires a number")
    return value


def truthy(value: object) -> bool:
    """Only false and nothing are falsey; every other Clarity value is truthy."""
    return value is not False and value is not None


def equal(left: object, right: object) -> bool:
    """Compare values without Python's ``True == 1`` equivalence."""
    if is_number(left) and is_number(right):
        return left == right
    if type(left) is not type(right):
        return False
    return left == right


def compare(left: object, right: object, operator: str) -> bool:
    if (is_number(left) and is_number(right)) or (isinstance(left, str) and isinstance(right, str)):
        return {
            ">": left > right,
            "<": left < right,
            ">=": left >= right,
            "<=": left <= right,
        }[operator]
    raise RuntimeError(f"{operator!r} requires two numbers or two strings")


def add(left: object, right: object) -> object:
    if isinstance(left, str) or isinstance(right, str):
        return stringify(left) + stringify(right)
    return require_number(left, "'+'") + require_number(right, "'+'")


def subtract(left: object, right: object) -> object:
    return require_number(left, "'-'") - require_number(right, "'-'")


def multiply(left: object, right: object) -> object:
    return require_number(left, "'*'") * require_number(right, "'*'")


def divide(left: object, right: object) -> object:
    divisor = require_number(right, "'/'")
    if divisor == 0:
        raise RuntimeError("Cannot divide by zero")
    return require_number(left, "'/'") / divisor


def remainder(left: object, right: object) -> object:
    divisor = require_number(right, "'%'")
    if divisor == 0:
        raise RuntimeError("Cannot divide by zero")
    return require_number(left, "'%'") % divisor


def stringify(value: object) -> str:
    if value is None: return "nothing"
    if value is True: return "true"
    if value is False: return "false"
    if isinstance(value, str): return value
    if isinstance(value, ClarityFunction): return f"<function {value.display_name()}>"
    if isinstance(value, list): return "[" + ", ".join(_literal_string(item) for item in value) + "]"
    if isinstance(value, dict):
        pairs = (f"{_literal_string(key)}: {_literal_string(item)}" for key, item in value.items())
        return "{" + ", ".join(pairs) + "}"
    return str(value)


def validate_dictionary_key(value: object) -> object:
    if isinstance(value, (list, dict)):
        raise RuntimeError("Dictionary keys must be numbers, strings, booleans, or nothing")
    return value


def _literal_string(value: object) -> str:
    if isinstance(value, str): return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'
    return stringify(value)
