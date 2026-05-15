"""Коллекция с поддержкой стратегий для ЛР-5.

Класс `StrategyCollection` — упрощённая коллекция, которая хранит объекты
и предоставляет методы `sort_by`, `filter_by`, `apply`, `map`, а также
цепочку операций (возвращает self для удобного чейнинга).
"""
from __future__ import annotations

from typing import Iterable, Callable, List, TypeVar, Generic

T = TypeVar("T")


class StrategyCollection(Generic[T]):
    def __init__(self, items: Iterable[T] | None = None) -> None:
        self._items: List[T] = list(items) if items is not None else []

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

    def add(self, item: T) -> None:
        self._items.append(item)

    def extend(self, items: Iterable[T]) -> None:
        self._items.extend(items)

    def to_list(self) -> List[T]:
        return list(self._items)

    # --- функции высокого уровня ---
    def sort_by(self, key_func: Callable[[T], object], reverse: bool = False) -> "StrategyCollection[T]":
        """Сортирует коллекцию на месте по ключевой функции и возвращает self."""
        self._items.sort(key=key_func, reverse=reverse)  # type: ignore[arg-type]
        return self

    def filter_by(self, predicate: Callable[[T], bool]) -> "StrategyCollection[T]":
        """Фильтрует коллекцию (на месте) и возвращает self."""
        self._items = [i for i in self._items if predicate(i)]
        return self

    def apply(self, func: Callable[[T], T]) -> "StrategyCollection[T]":
        """Применяет функцию ко всем элементам коллекции (мутация возможна).

        Функция должна принимать элемент и возвращать его (или новый).
        """
        self._items = [func(i) for i in self._items]
        return self

    def map(self, func: Callable[[T], object]) -> List[object]:
        """Возвращает результат map(func, items) как список (не меняет коллекцию)."""
        return list(map(func, self._items))

    # удобные методы для демонстрации
    def print_preview(self, n: int = 10) -> None:
        for i, item in enumerate(self._items[:n], start=1):
            print(f" {i:2d}) {item}")

    def __repr__(self) -> str:
        return f"StrategyCollection(len={len(self)})"