"""Стратегии и функции-обработчики для ЛР-5.

Здесь собраны функции и callable-объекты для сортировки, фильтрации
и обработки объектов коллекции (на базе банковских счетов из ЛР-3).
"""
from __future__ import annotations

from typing import Callable, Any


def by_owner_name(item: Any) -> str:
    """Ключ для сортировки по имени владельца.

    Возвращает строку с именем владельца (owner_name).
    """
    return getattr(item, "owner_name", "")


def by_balance(item: Any) -> float:
    """Ключ для сортировки по текущему балансу.

    Возвращает float баланс (если атрибута нет — 0.0).
    """
    return float(getattr(item, "balance", 0.0) or 0.0)


def by_balance_then_owner(item: Any) -> tuple:
    """Ключ для сортировки сначала по балансу, затем по имени владельца."""
    return (by_balance(item), by_owner_name(item))


def is_rich(min_balance: float) -> Callable[[Any], bool]:
    """Фабрика: создаёт предикат, который проверяет, что баланс >= min_balance.

    Использование:
        rich_filter = is_rich(100000)
        rich_list = list(filter(rich_filter, accounts))
    """

    def predicate(item: Any) -> bool:
        return by_balance(item) >= float(min_balance)

    return predicate


def is_savings_account(item: Any) -> bool:
    """Фильтр: True для объектов типа SavingsAccount (по имени класса).

    Используем простую проверку на имя класса, чтобы не жестко зависеть от
    структуры пакета. Если в проекте доступен класс SavingsAccount, лучше
    использовать isinstance.
    """
    cls_name = item.__class__.__name__
    return cls_name == "SavingsAccount"


def _shift_balance(item: Any, factor: float) -> Any:
    """Изменяет баланс объекта до значения balance * factor через его методы.

    Возвращает сам объект. Если у объекта нет подходящих методов, возвращает
    его без изменений.
    """
    if not hasattr(item, "balance"):
        return item

    try:
        current = float(item.balance)
        target = current * float(factor)
        delta = target - current

        if abs(delta) < 1e-12:
            return item

        if delta > 0:
            if hasattr(item, "deposit"):
                item.deposit(delta, "Стратегия: изменение баланса")
        else:
            amount = abs(delta)
            if hasattr(item, "withdraw"):
                item.withdraw(amount, "Стратегия: изменение баланса")
        return item
    except Exception:
        return item


def make_balance_multiplier(factor: float) -> Callable[[Any], Any]:
    """Фабрика функций: создаёт функцию, которая умножает баланс объекта на фактор.

    Возвращаемая функция изменяет объект на месте и возвращает его.
    """

    def multiplier(item: Any) -> Any:
        return _shift_balance(item, factor)

    return multiplier


class PercentBonusStrategy:
    """Callable-объект: добавляет процентную надбавку к балансу.

    Пример:
        strategy = PercentBonusStrategy(0.05)  # +5%
        collection.apply(strategy)
    """

    def __init__(self, percent: float) -> None:
        self.percent = float(percent)

    def __call__(self, item: Any) -> Any:
        return _shift_balance(item, 1.0 + self.percent)


def owner_to_string(item: Any) -> str:
    """Функция для map(): превращает объект в строку с именем и балансом."""
    return f"{getattr(item, 'owner_name', '?')}: {getattr(item, 'balance', 0):.2f}"
