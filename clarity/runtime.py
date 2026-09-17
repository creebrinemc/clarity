from collections.abc import Callable
from dataclasses import dataclass
from typing import TYPE_CHECKING

from . import ast
from .errors import RuntimeError
from .source import SourceSpan

if TYPE_CHECKING:
    from .environment import Environment


@dataclass(slots=True)
class ClarityFunction:
    name: str | None
    parameters: tuple[ast.Parameter, ...]
    body: ast.BlockNode
    closure: "Environment"
    span: SourceSpan

    def display_name(self) -> str:
        return self.name or "anonymous"


@dataclass(slots=True)
class ClarityNativeFunction:
    name: str
    func: Callable[..., object]
    min_arity: int
    max_arity: int | None = None  # None means exactly min_arity, -1 means variadic >= min_arity
    doc: str = ""

    def display_name(self) -> str:
        return self.name

    def call(self, arguments: list[object]) -> object:
        arg_count = len(arguments)
        if self.max_arity is None:
            if arg_count != self.min_arity:
                raise RuntimeError(
                    f"Function '{self.name}' expects {self.min_arity} argument(s), got {arg_count}"
                )
        elif self.max_arity == -1:
            if arg_count < self.min_arity:
                raise RuntimeError(
                    f"Function '{self.name}' expects at least {self.min_arity} argument(s), got {arg_count}"
                )
        else:
            if not (self.min_arity <= arg_count <= self.max_arity):
                if self.min_arity == self.max_arity:
                    raise RuntimeError(
                        f"Function '{self.name}' expects {self.min_arity} argument(s), got {arg_count}"
                    )
                raise RuntimeError(
                    f"Function '{self.name}' expects between {self.min_arity} and {self.max_arity} argument(s), got {arg_count}"
                )
        return self.func(*arguments)


def _dict_key(key: object) -> tuple[type, object]:
    if isinstance(key, bool):
        return (bool, key)
    if isinstance(key, (int, float)):
        if isinstance(key, int) or key.is_integer():
            return (int, int(key))
        return (float, key)
    return (type(key), key)


class ClarityDict(dict):
    """A dictionary implementation preserving distinct types (e.g. 1 vs True)."""

    def __init__(self, entries=None):
        super().__init__()
        self._data: dict[tuple[type, object], tuple[object, object]] = {}
        if entries:
            for k, v in entries:
                self[k] = v

    def __getitem__(self, key: object) -> object:
        k = _dict_key(key)
        if k not in self._data:
            raise KeyError(key)
        return self._data[k][1]

    def __setitem__(self, key: object, value: object) -> None:
        self._data[_dict_key(key)] = (key, value)

    def __contains__(self, key: object) -> bool:
        return _dict_key(key) in self._data

    def __iter__(self):
        return (k for k, v in self._data.values())

    def __len__(self) -> int:
        return len(self._data)

    def items(self):
        return (val for val in self._data.values())

    def keys(self):
        return (k for k, v in self._data.values())

    def values(self):
        return (v for k, v in self._data.values())

    def get(self, key: object, default: object = None) -> object:
        k = _dict_key(key)
        if k in self._data:
            return self._data[k][1]
        return default

    def __eq__(self, other: object) -> bool:
        if isinstance(other, ClarityDict):
            return self._data == other._data
        if isinstance(other, dict):
            if len(self) != len(other):
                return False
            for k, v in self.items():
                if k not in other or other[k] != v:
                    return False
            return True
        return False

    def __repr__(self) -> str:
        pairs = [f"{k!r}: {v!r}" for k, v in self.items()]
        return "{" + ", ".join(pairs) + "}"

