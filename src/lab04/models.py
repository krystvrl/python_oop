"""Модели ЛР-4: банковские счета, реализующие интерфейсы Printable и Comparable."""

from __future__ import annotations

import sys
from functools import cmp_to_key
from pathlib import Path
from typing import Iterable, List


def _ensure_src_on_path() -> None:
    src_dir = Path(__file__).resolve().parents[1]
    lab03_dir = src_dir / "lab03"

    for path in (src_dir, lab03_dir):
        if str(path) not in sys.path:
            sys.path.insert(0, str(path))


_ensure_src_on_path()

from lab03.base import BankAccount as BaseBankAccount  # noqa: E402
from lab03.models import CreditAccount as BaseCreditAccount  # noqa: E402
from lab03.models import SavingsAccount as BaseSavingsAccount  # noqa: E402

from lab04.interfaces import Comparable, Printable  # noqa: E402


class PrintableMixin(Printable):
    """Вспомогательная реализация __str__ через интерфейс Printable."""

    def __str__(self) -> str:
        return self.to_string()


class ComparableMixin(Comparable):
    """Вспомогательная реализация compare_to через числовой ключ сравнения."""

    def _comparison_value(self) -> float:
        raise NotImplementedError

    def compare_to(self, other: object) -> int:
        if not isinstance(other, ComparableMixin):
            raise TypeError("Сравнение возможно только с объектом, реализующим Comparable")

        left = self._comparison_value()
        right = other._comparison_value()
        return (left > right) - (left < right)


class BankAccount(BaseBankAccount, PrintableMixin, ComparableMixin):
    """Базовый банковский счет с интерфейсами Printable и Comparable."""

    def to_string(self) -> str:
        info = self.get_account_info()
        return (
            "🏦 BankAccount\n"
            f"   Номер счета: {info['account_number']}\n"
            f"   Владелец: {info['owner_name']}\n"
            f"   Баланс: {info['balance']:.2f} {info['currency']}\n"
            f"   Статус: {info['status']}\n"
            f"   Годовой доход: {self.calculate_annual_interest():.2f} {self.currency}"
        )

    def _comparison_value(self) -> float:
        return float(self.balance)


class SavingsAccount(BaseSavingsAccount, PrintableMixin, ComparableMixin):
    """Сберегательный счет, реализующий интерфейсы."""

    def to_string(self) -> str:
        base_text = super().__str__()
        return (
            f"{base_text}\n"
            f"   [Interface] Printable: доступен\n"
            f"   [Interface] Сравнение по балансу + процентам: {self._comparison_value():.2f}"
        )

    def _comparison_value(self) -> float:
        return float(self.balance + self.calculate_annual_interest())


class CreditAccount(BaseCreditAccount, PrintableMixin, ComparableMixin):
    """Кредитный счет, реализующий интерфейсы."""

    def to_string(self) -> str:
        base_text = super().__str__()
        return (
            f"{base_text}\n"
            f"   [Interface] Printable: доступен\n"
            f"   [Interface] Сравнение по балансу с учетом долга: {self._comparison_value():.2f}"
        )

    def _comparison_value(self) -> float:
        return float(self.balance + self.calculate_annual_interest())


class InterfaceCollection:
    """Коллекция объектов, работающих через интерфейсы Printable и Comparable."""

    def __init__(self) -> None:
        self._items: List[PrintableMixin] = []

    def add(self, item: PrintableMixin) -> None:
        if not isinstance(item, Printable) or not isinstance(item, Comparable):
            raise TypeError("Коллекция принимает только объекты, реализующие Printable и Comparable")
        self._items.append(item)

    def get_all(self) -> List[PrintableMixin]:
        return self._items.copy()

    def get_printable(self) -> List[PrintableMixin]:
        return [item for item in self._items if isinstance(item, Printable)]

    def get_comparable(self) -> List[PrintableMixin]:
        return [item for item in self._items if isinstance(item, Comparable)]

    def sort_by_interface(self, reverse: bool = False) -> None:
        self._items.sort(key=cmp_to_key(lambda left, right: left.compare_to(right)), reverse=reverse)

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

    def __getitem__(self, index: int) -> PrintableMixin:
        return self._items[index]


def print_all(items: Iterable[Printable]) -> None:
    """Универсальная функция печати через интерфейс Printable."""
    for item in items:
        print(item.to_string())
        print("-" * 60)


def sort_by_interface(items: Iterable[Comparable], reverse: bool = False) -> List[Comparable]:
    """Универсальная сортировка через интерфейс Comparable."""
    sorted_items = sorted(list(items), key=cmp_to_key(lambda left, right: left.compare_to(right)), reverse=reverse)
    return sorted_items