"""Registries: every pluggable part of the benchmark is looked up by name.

    from marathonts.bench import registry as R
    from marathonts.bench.models import BaseModel

    @R.models.register("my_model")
    class MyModel(BaseModel): ...

Registries: `datasets`, `tasks`, `pool_generators`, `long_generators`, `assemblers`, `joiners`,
`methods`, `models`, `fidelity_metrics`, `utility_metrics`. The hypothesis part has its own for statistical
tests and hypotheses (`hypotheses.stats.DATASET_TESTS` and `GLOBAL_TESTS`, `hypotheses.catalog.HYPOTHESES`).
"""
from __future__ import annotations

from typing import Any, Callable, Iterator


class Registry:
    def __init__(self, kind: str):
        self.kind = kind
        self._items: dict[str, Any] = {}

    def register(self, name: str, obj: Any = None, *, overwrite: bool = False):
        """`registry.register("x", obj)` or as a decorator `@registry.register("x")`."""
        def put(o):
            if name in self._items and not overwrite:
                raise KeyError(f"{self.kind} '{name}' is already registered (pass overwrite=True)")
            self._items[name] = o
            return o

        return put(obj) if obj is not None else put

    def get(self, name: str) -> Any:
        if name not in self._items:
            raise KeyError(f"unknown {self.kind} '{name}'. Registered: {sorted(self._items)}")
        return self._items[name]

    def __contains__(self, name: str) -> bool:
        return name in self._items

    def __iter__(self) -> Iterator[str]:
        return iter(self._items)

    def items(self):
        return self._items.items()

    def names(self) -> list[str]:
        return list(self._items)

    def __repr__(self) -> str:
        return f"Registry({self.kind}: {sorted(self._items)})"


datasets = Registry("dataset")
tasks = Registry("task")
pool_generators = Registry("pool generator")
long_generators = Registry("long generator")
assemblers = Registry("assembler")
joiners = Registry("joiner")
methods = Registry("method")
models = Registry("model")
fidelity_metrics = Registry("fidelity metric group")
utility_metrics = Registry("utility metric")


def load_builtins() -> None:
    """Import the modules whose import registers the built-in components."""
    import importlib

    for mod in ("tasks", "datasets", "generators.builtin", "assemblers", "joiners", "methods", "models", "fidelity",
                "utility"):
        importlib.import_module(f"{__package__}.{mod}")


Factory = Callable[..., Any]
