"""Variable storage for Clarity execution."""

from .errors import RuntimeError


class Environment:
    """A scope-ready variable environment. Parent scopes are supported internally."""
    def __init__(self, parent: "Environment | None" = None):
        self.values: dict[str, object] = {}
        self.parent = parent

    def define(self, name: str, value: object) -> None: self.values[name] = value

    def assign(self, name: str, value: object) -> None:
        """Replace the nearest binding, or define one in this environment."""
        environment = self._find(name)
        (environment or self).values[name] = value

    def get(self, name: str) -> object:
        environment = self._find(name)
        if environment is None: raise RuntimeError(f"Unknown variable: {name}")
        return environment.values[name]

    def set(self, name: str, value: object) -> None:
        environment = self._find(name)
        if environment is None: raise RuntimeError(f"Unknown variable: {name}")
        environment.values[name] = value

    def _find(self, name: str) -> "Environment | None":
        if name in self.values: return self
        return self.parent._find(name) if self.parent else None
