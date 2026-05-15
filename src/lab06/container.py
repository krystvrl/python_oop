from __future__ import annotations

from typing import (
    TypeVar,
    Generic,
    Callable,
    Optional,
    Protocol,
    List,
)

# Protocols (structural typing)


class Displayable(Protocol):
    def display(self) -> str:
        ...


class Scorable(Protocol):
    def score(self) -> float:
        ...


# Type variables
T = TypeVar("T")
R = TypeVar("R")
D = TypeVar("D", bound=Displayable)
S = TypeVar("S", bound=Scorable)


class TypedCollection(Generic[T]):
    """Generic-коллекция с простыми helper-методами и валидацией.

    Аргументы:
        validator: необязательная функция для runtime-проверки элемента при добавлении.
                   Если задана и возвращает False — `add()` вызовет TypeError.
    """

    def __init__(self, *, validator: Optional[Callable[[T], bool]] = None) -> None:
        self._items: List[T] = []
        self._validator = validator

    def add(self, item: T) -> None:
        if self._validator is not None and not self._validator(item):
            raise TypeError("Item does not satisfy collection validator")
        self._items.append(item)

    def remove(self, item: T) -> None:
        self._items.remove(item)

    def to_list(self) -> List[T]:
        return list(self._items)

    # --- find / filter / map ---
    def find(self, predicate: Callable[[T], bool]) -> Optional[T]:
        for item in self._items:
            if predicate(item):
                return item
        return None

    def filter(self, predicate: Callable[[T], bool]) -> List[T]:
        return [item for item in self._items if predicate(item)]

    def map(self, transform: Callable[[T], R]) -> List[R]:
        return [transform(item) for item in self._items]

   
    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self):
        return iter(self._items)



class DisplayableCollection(TypedCollection[D], Generic[D]):
    pass


class ScorableCollection(TypedCollection[S], Generic[S]):
    pass

