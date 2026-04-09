#!/usr/bin/env python3
"""
Демонстрация работы лабораторной работы №3.
Вариант 4: SavingsAccount и CreditAccount.
"""

from base import BankAccount
from models import SavingsAccount, CreditAccount


def print_separator(title: str = ""):
    """Вывод разделителя с заголовком."""
    print("\n" + "=" * 60)
    if title:
        print(f"📌 {title}")
    print("=" * 60)


def demo_inheritance():
    """Сценарий 1: Демонстрация наследования."""
    print_separator("СЦЕНАРИЙ 1: Наследование и использование super()")
    
    regular = BankAccount("Нестеров Павел Владимирович", "RUB", 5000)
    savings = SavingsAccount("Маленкова Анна Викторовна", "RUB", 10000, interest_rate=6.5)
    credit = CreditAccount("Москвитин Алексей Андреевич", "RUB", credit_limit=100000)
    
    print("\n🔹 Созданы счета:")
    print(regular)
    print("\n" + "-" * 40)
    print(savings)
    print("\n" + "-" * 40)
    print(credit)
    
    print("\n📊 Демонстрация работы методов:")
    
    # Сберегательный счет
    print(f"\n💰 Сберегательный счет Маленковой:")
    print(f"   Баланс: {savings.balance:.2f} {savings.currency}")
    print(f"   Процентная ставка: {savings.interest_rate}%")
    interest = savings.apply_interest()
    print(f"   Начислено процентов: {interest:.2f} {savings.currency}")
    print(f"   Баланс после начисления: {savings.balance:.2f} {savings.currency}")
    
    # Кредитный счет
    print(f"\n💳 Кредитный счет Москвитина:")
    print(f"   Кредитный лимит: {credit.credit_limit:.2f} {credit.currency}")
    print(f"   Доступно кредита: {credit.available_credit:.2f} {credit.currency}")
    print(f"   Баланс до снятия: {credit.balance:.2f}")
    
    credit.withdraw(15000, "Покупка ноутбука")
    print(f"   После снятия 15000:")
    print(f"   Баланс: {credit.balance:.2f} {credit.currency}")
    print(f"   Использовано кредита: {credit.credit_used:.2f} {credit.currency}")
    
    credit.deposit(10000, "Пополнение")
    print(f"\n   После пополнения на 10000:")
    print(f"   Баланс: {credit.balance:.2f} {credit.currency}")
    print(f"   Остаток кредита: {credit.credit_used:.2f} {credit.currency}")


def demo_polymorphism():
    """Сценарий 2: Демонстрация полиморфизма."""
    print_separator("СЦЕНАРИЙ 2: Полиморфизм — один метод, разное поведение")
    
    accounts = [
        BankAccount("Морозова Ольга Сергеевна", "RUB", 50000),
        SavingsAccount("Кудрявцева Нина Анатольевна", "RUB", 200000, interest_rate=7.0),
        CreditAccount("Волохин Дмитрий Николаевич", "RUB", credit_limit=300000),
    ]
    
    print("\n📋 Коллекция счетов:")
    for acc in accounts:
        print(f"   {acc.__class__.__name__}: {acc.owner_name} — {acc.balance:.2f} {acc.currency}")
    
    print("\n💰 Расчет годового дохода (полиморфизм):")
    for acc in accounts:
        income = acc.calculate_annual_income()
        print(f"   {acc.__class__.__name__}: доход = {income:+.2f} {acc.currency}")
    
    print("\n🔍 Проверка типов (isinstance):")
    for acc in accounts:
        print(f"   {acc.owner_name}:")
        print(f"      - является BankAccount: {isinstance(acc, BankAccount)}")
        print(f"      - является SavingsAccount: {isinstance(acc, SavingsAccount)}")
        print(f"      - является CreditAccount: {isinstance(acc, CreditAccount)}")


def demo_collection():
    """Сценарий 3: Фильтрация коллекции."""
    print_separator("СЦЕНАРИЙ 3: Фильтрация коллекции по типу")
    
    accounts = [
        BankAccount("Бреднева Ирина Тимофеевна", "USD", 1000),
        SavingsAccount("Новикова Зоя Владимировна", "RUB", 150000, interest_rate=6.0),
        CreditAccount("Федорова Мария Олеговна", "EUR", credit_limit=50000),
        SavingsAccount("Лебедева Анна Павловна", "RUB", 50000, interest_rate=7.5),
        CreditAccount("Жуков Денис Александрович", "RUB", credit_limit=200000),
    ]
    
    def get_savings(acc_list):
        return [a for a in acc_list if isinstance(a, SavingsAccount)]
    
    def get_credits(acc_list):
        return [a for a in acc_list if isinstance(a, CreditAccount)]
    
    print(f"\n📊 Всего счетов: {len(accounts)}")
    
    savings = get_savings(accounts)
    print(f"\n🏦 Сберегательные счета ({len(savings)} шт.):")
    for acc in savings:
        print(f"   - {acc.owner_name}: {acc.balance:.2f} {acc.currency} (ставка {acc.interest_rate}%)")
    
    credits = get_credits(accounts)
    print(f"\n💳 Кредитные счета ({len(credits)} шт.):")
    for acc in credits:
        print(f"   - {acc.owner_name}: лимит {acc.credit_limit:.2f} {acc.currency}")


def main():
    print("=" * 60)
    print("🏦 ЛАБОРАТОРНАЯ РАБОТА №3 — Вариант 4")
    print("   Наследование и иерархия классов")
    print("   Базовый класс: BankAccount")
    print("   Дочерние классы: SavingsAccount, CreditAccount")
    print("=" * 60)
    
    demo_inheritance()
    demo_polymorphism()
    demo_collection()
    
    print_separator("ВЫВОДЫ")
    print("""
    ✅ Изучено:
    1. Наследование — super(), новые атрибуты, новые методы
    2. Полиморфизм — переопределение __str__, withdraw, deposit, calculate_annual_income
    3. isinstance() — проверка типов и фильтрация
    4. Работа с коллекцией объектов разных типов
    """)


if __name__ == "__main__":
    main()