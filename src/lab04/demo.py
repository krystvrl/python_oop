#!/usr/bin/env python3
"""Демонстрация лабораторной работы №4: интерфейсы и абстрактные классы."""

from __future__ import annotations

import sys
from pathlib import Path


def _ensure_src_on_path() -> None:
    src_dir = Path(__file__).resolve().parents[1]
    if str(src_dir) not in sys.path:
        sys.path.insert(0, str(src_dir))


_ensure_src_on_path()

from lab04.interfaces import Comparable, Printable  # noqa: E402
from lab04.models import (  # noqa: E402
    BankAccount,
    CreditAccount,
    InterfaceCollection,
    SavingsAccount,
    print_all,
    sort_by_interface,
)


def print_separator(title: str) -> None:
    print("\n" + "=" * 72)
    print(f"📌 {title}")
    print("=" * 72)


def scenario_1_interfaces_and_isinstance() -> None:
    print_separator("Сценарий 1: интерфейсы и isinstance")

    accounts = [
        BankAccount("Иванов Иван Иванович", "RUB", 12000),
        SavingsAccount("Петров Петр Петрович", "RUB", 25000, interest_rate=7.5),
        CreditAccount("Сидорова Анна Павловна", "RUB", credit_limit=75000, interest_on_debt=18.0),
    ]

    for account in accounts:
        print(account.to_string())
        print(f"   isinstance(..., Printable): {isinstance(account, Printable)}")
        print(f"   isinstance(..., Comparable): {isinstance(account, Comparable)}")
        print()


def scenario_2_interface_functions() -> None:
    print_separator("Сценарий 2: универсальные функции через интерфейс")

    accounts = [
        BankAccount("Орлова Мария Сергеевна", "USD", 5000),
        SavingsAccount("Кузнецов Алексей Игоревич", "RUB", 150000, interest_rate=6.0),
        CreditAccount("Фролов Денис Викторович", "EUR", credit_limit=40000, interest_on_debt=12.5),
    ]

    print("Вывод через print_all(items: list[Printable]):")
    print_all(accounts)

    print("Сортировка через sort_by_interface(items: list[Comparable]):")
    sorted_accounts = sort_by_interface(accounts)
    for account in sorted_accounts:
        print(f"   {account.__class__.__name__}: {account.to_string().splitlines()[0]}")


def scenario_3_collection_and_filtering() -> None:
    print_separator("Сценарий 3: коллекция и фильтрация по интерфейсам")

    collection = InterfaceCollection()
    collection.add(BankAccount("Александров Никита Олегович", "RUB", 30000))
    collection.add(SavingsAccount("Михайлова Ольга Викторовна", "RUB", 100000, interest_rate=8.0))
    collection.add(CreditAccount("Николаев Денис Артемович", "USD", credit_limit=90000, interest_on_debt=15.0))

    print(f"Всего объектов в коллекции: {len(collection)}")
    print("\nФильтрация get_printable():")
    for item in collection.get_printable():
        print(f"   {item.__class__.__name__}")

    print("\nФильтрация get_comparable():")
    for item in collection.get_comparable():
        print(f"   {item.__class__.__name__}")

    print("\nИтерация по коллекции:")
    for item in collection:
        print(f"   {item.to_string().splitlines()[0]}")

    print("\nСортировка коллекции по интерфейсному сравнению:")
    collection.sort_by_interface()
    for item in collection:
        print(f"   {item.__class__.__name__}: {item.to_string().splitlines()[0]}")


def main() -> None:
    print("=" * 72)
    print("🏦 Лабораторная работа №4 — Интерфейсы и абстрактные классы (вариант 4)")
    print("   Реализованы Printable и Comparable")
    print("   Классы: BankAccount, SavingsAccount, CreditAccount")
    print("=" * 72)

    scenario_1_interfaces_and_isinstance()
    scenario_2_interface_functions()
    scenario_3_collection_and_filtering()

    print_separator("Вывод")
    print(
        """
        ✅ Изучено:
        1. ABC и интерфейсы как контракт поведения
        2. Реализация нескольких интерфейсов в одних и тех же классах
        3. Использование `isinstance()` для проверки интерфейсов
        4. Универсальные функции, работающие через интерфейсы
        5. Фильтрация и сортировка коллекции по интерфейсам
        """.strip()
    )


if __name__ == "__main__":
    main()