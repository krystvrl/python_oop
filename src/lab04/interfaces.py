"""Интерфейсы для лабораторной работы №4."""

from __future__ import annotations

from abc import ABC, abstractmethod


class Printable(ABC):
    """Интерфейс для объектов, которые можно преобразовать в строку."""

    @abstractmethod
    def to_string(self) -> str:
        """Вернуть строковое представление объекта."""

    def __str__(self) -> str:
        return self.to_string()


class Comparable(ABC):
    """Интерфейс для объектов, которые можно сравнивать."""

    @abstractmethod
    def compare_to(self, other: object) -> int:
        """Сравнить объект с другим: -1, 0 или 1."""
