#!/usr/bin/env python3
"""Демонстрация ЛР-5 — функции как аргументы, стратегии и делегаты.

Три сценария:
1) Полная цепочка filter -> sort -> apply
2) Три стратегии сортировки на одной коллекции
3) callable-объект как стратегия + map/filter + lambda

Файлы, используемые: `strategies.py`, `collection.py`, и классы из ЛР-3
(BankAccount, SavingsAccount, CreditAccount).
"""
from __future__ import annotations

import sys
from pathlib import Path


def _ensure_src_on_path() -> None:
    src_dir = Path(__file__).resolve().parents[1]
    if str(src_dir) not in sys.path:
        sys.path.insert(0, str(src_dir))


_ensure_src_on_path()

from lab05.collection import StrategyCollection  
from lab05 import strategies  
# импортируем модели из ЛР-3 (должны существовать в проекте)
try:
    from lab03.base import BankAccount 
    from lab03.models import SavingsAccount, CreditAccount  
except Exception:
    # если пакеты устроены иначе и модули используют имена без пакета
    # — добавим прямо путь к папке lab03 и попытаемся импортировать локально
    from pathlib import Path as _P

    _lab03_dir = _P(__file__).resolve().parents[1] / "lab03"
    if str(_lab03_dir) not in sys.path:
        sys.path.insert(0, str(_lab03_dir))
    from base import BankAccount  # type: ignore
    from models import SavingsAccount, CreditAccount  # type: ignore


def print_header(title: str) -> None:
    print('\n' + '=' * 72)
    print(f" {title}")
    print('=' * 72)


def only_savings_account(item: object) -> bool:
    """Фильтр по типу: True только для SavingsAccount."""
    return isinstance(item, SavingsAccount)


def scenario_1_chain_operations() -> None:
    print_header("Сценарий 1: filter -> sort -> apply (цепочка)")

    col = StrategyCollection()
    col.add(BankAccount("Александров", "RUB", 30000))
    col.add(SavingsAccount("Михайлова", "RUB", 100000, interest_rate=8.0))
    col.add(CreditAccount("Николаев", "USD", credit_limit=90000))
    col.add(SavingsAccount("Орлова", "RUB", 50000, interest_rate=6.0))
    col.add(BankAccount("Петров", "EUR", 12000))

    print("Исходная коллекция:")
    col.print_preview()

    # создаём фильтр (с помощью фабрики) — оставляем только богатых
    rich_filter = strategies.is_rich(40000)

    # применяем цепочку: фильтр, сортировка по балансу, и затем процентная надбавка
    col.filter_by(rich_filter).sort_by(strategies.by_balance).apply(strategies.PercentBonusStrategy(0.05))

    print('\nПосле filter_by(is_rich(40000)) -> sort_by(by_balance) -> apply(+5%):')
    col.print_preview()


def scenario_2_sort_strategies() -> None:
    print_header("Сценарий 2: Три стратегии сортировки")

    base_accounts = [
        BankAccount("Кузнецов", "RUB", 45000),
        BankAccount("Иванов", "RUB", 45000),
        BankAccount("Сидоров", "RUB", 80000),
        BankAccount("Петров", "RUB", 12000),
    ]

    col_by_name = StrategyCollection(list(base_accounts))
    col_by_balance = StrategyCollection(list(base_accounts))
    col_by_balance_then_owner = StrategyCollection(list(base_accounts))

    print("Сортировка по имени:")
    col_by_name.sort_by(strategies.by_owner_name)
    col_by_name.print_preview()

    print('\nСортировка по балансу:')
    col_by_balance.sort_by(strategies.by_balance)
    col_by_balance.print_preview()

    print('\nСортировка по балансу и имени:')
    col_by_balance_then_owner.sort_by(strategies.by_balance_then_owner)
    col_by_balance_then_owner.print_preview()


def scenario_3_callable_strategy_and_map_filter() -> None:
    print_header("Сценарий 3: callable-стратегия и использование map/filter")

    col = StrategyCollection([
        SavingsAccount("Кудрявцева", "RUB", 200000, interest_rate=7.0),
        CreditAccount("Волохин", "RUB", credit_limit=300000),
        BankAccount("Морозова", "RUB", 50000),
    ])

    # Дадим кредитному счёту положительный остаток, чтобы изменение баланса было видно
    col.to_list()[1].deposit(50000, "Стартовый взнос")

    print("Исходная коллекция:")
    col.print_preview()

    # callable-объект как стратегия — уменьшаем баланс на 10% у всех
    multiplier = strategies.make_balance_multiplier(0.9)
    col.apply(multiplier)
    print('\nПосле применения make_balance_multiplier(0.9):')
    col.print_preview()

    # покажем map() — превращаем в строки owner: balance
    owner_lines_named = col.map(strategies.owner_to_string)
    owner_lines_lambda = col.map(lambda item: f"{item.owner_name}: {item.balance:.2f}")
    print('\nРезультат map(owner_to_string):')
    for line in owner_lines_named:
        print('  ', line)
    print('\nРезультат map(lambda ...):')
    for line in owner_lines_lambda:
        print('  ', line)

    # использование встроенного filter() и фильтра по типу
    rich_filter = strategies.is_rich(100000)
    savings_named = list(filter(only_savings_account, col.to_list()))
    savings_lambda = list(filter(lambda item: isinstance(item, SavingsAccount), col.to_list()))
    rich_accounts = list(filter(rich_filter, col.to_list()))

    print(f"\nПосле встроенного filter(is_rich(100000)) — найдено {len(rich_accounts)}")
    for it in rich_accounts:
        print('  ', getattr(it, 'owner_name', '---'), getattr(it, 'balance', 0))

    print(f"\nФильтр по типу через named function — найдено {len(savings_named)}")
    print(f"Фильтр по типу через lambda — найдено {len(savings_lambda)}")


def main() -> None:
    print('=' * 72)
    print('Лабораторная работа №5 — Функции как аргументы. Вариант 4')
    print('=' * 72)

    scenario_1_chain_operations()
    scenario_2_sort_strategies()
    scenario_3_callable_strategy_and_map_filter()


if __name__ == '__main__':
    main()

