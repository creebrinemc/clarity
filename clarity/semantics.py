"""Explicit runtime rules for the currently supported Clarity values."""

from .errors import RuntimeError
from .runtime import ClarityFunction, ClarityNativeFunction


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
    if isinstance(value, (ClarityFunction, ClarityNativeFunction)): return f"<function {value.display_name()}>"
    if isinstance(value, list): return "[" + ", ".join(_literal_string(item) for item in value) + "]"
    if isinstance(value, dict):
        pairs = (f"{_literal_string(key)}: {_literal_string(item)}" for key, item in value.items())
        return "{" + ", ".join(pairs) + "}"
    return str(value)


def validate_dictionary_key(value: object) -> object:
    if isinstance(value, (list, dict)):
        raise RuntimeError("Dictionary keys must be numbers, strings, booleans, or nothing")
    return value


def type_name(value: object) -> str:
    if value is None: return "nothing"
    if isinstance(value, bool): return "boolean"
    if is_number(value): return "number"
    if isinstance(value, str): return "string"
    if isinstance(value, list): return "list"
    if isinstance(value, dict): return "dictionary"
    if isinstance(value, (ClarityFunction, ClarityNativeFunction)): return "function"
    return type(value).__name__


def require_integer_index(value: object, container_type: str) -> int:
    if is_number(value) and (isinstance(value, int) or value.is_integer()):
        return int(value)
    raise RuntimeError(f"{container_type} index must be an integer")


def get_index(target: object, index: object) -> object:
    if isinstance(target, list):
        idx = require_integer_index(index, "List")
        if idx < 0 or idx >= len(target):
            raise RuntimeError(f"List index out of range: {idx}")
        return target[idx]
    if isinstance(target, str):
        idx = require_integer_index(index, "String")
        if idx < 0 or idx >= len(target):
            raise RuntimeError(f"String index out of range: {idx}")
        return target[idx]
    if isinstance(target, dict):
        validate_dictionary_key(index)
        if index not in target:
            raise RuntimeError(f"Key not found: {_literal_string(index)}")
        return target[index]
    raise RuntimeError(f"Cannot index {type_name(target)}")


def set_index(target: object, index: object, value: object) -> None:
    if isinstance(target, list):
        idx = require_integer_index(index, "List")
        if idx < 0 or idx >= len(target):
            raise RuntimeError(f"List index out of range: {idx}")
        target[idx] = value
        return
    if isinstance(target, dict):
        validate_dictionary_key(index)
        target[index] = value
        return
    if isinstance(target, str):
        raise RuntimeError("Cannot assign to string index")
    raise RuntimeError(f"Cannot assign to index of {type_name(target)}")


def _literal_string(value: object) -> str:
    if isinstance(value, str): return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'
    return stringify(value)

