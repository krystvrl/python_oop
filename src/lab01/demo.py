"""
Демонстрационный модуль для класса BankAccount.
Содержит сценарии использования, демонстрацию валидации,
логических состояний и изменения состояния.
"""

from model import BankAccount, AccountStatus
from datetime import datetime


def print_separator(title: str = ""):
    """Печать разделителя с заголовком."""
    print("\n" + "=" * 60)
    if title:
        print(f" {title} ".center(60, "="))
    print("=" * 60)


def demo_creation_and_basic_operations():
    """
    Сценарий 1: Создание счетов и базовые операции.
    Демонстрация создания объектов, пополнения, снятия, вывода информации.
    """
    print_separator("СЦЕНАРИЙ 1: СОЗДАНИЕ И БАЗОВЫЕ ОПЕРАЦИИ")
    
    # Создание счетов
    print("\n📝 Создание счетов:")
    account1 = BankAccount("Иванов Иван Иванович", "RUB", 10000)
    account2 = BankAccount("Петров Петр Петрович", "RUB", 5000)
    
    print(account1)
    print("\n" + str(account2))
    
    # Демонстрация свойств
    print("\n📊 Доступ к свойствам:")
    print(f"Номер счета 1: {account1.account_number}")
    print(f"Владелец счета 2: {account2.owner_name}")
    print(f"Баланс счета 1: {account1.balance:,.2f} {account1.currency}")
    print(f"Статус счета 2: {account2.status.value}")
    
    # Операции со счетами
    print("\n💰 Выполнение операций:")
    
    # Пополнение
    t1 = account1.deposit(5000, "Зарплата")
    print(f"Пополнение: +5 000 {account1.currency}")
    print(f"Новый баланс: {account1.balance:,.2f} {account1.currency}")
    
    # Снятие
    t2 = account1.withdraw(2000, "Покупка продуктов")
    print(f"\nСнятие: -2 000 {account1.currency}")
    print(f"Новый баланс: {account1.balance:,.2f} {account1.currency}")
    
    # Перевод
    print(f"\n💸 Перевод между счетами:")
    print(f"До перевода: Счет1 = {account1.balance:,.2f}, Счет2 = {account2.balance:,.2f}")
    
    account1.transfer(account2, 3000, "Долг")
    
    print(f"После перевода: Счет1 = {account1.balance:,.2f}, Счет2 = {account2.balance:,.2f}")
    
    # История транзакций
    print("\n📋 История транзакций счета 1:")
    for i, t in enumerate(account1.get_transaction_history(), 1):
        print(f"  {i}. {t['date'].strftime('%H:%M:%S')} - {t['type']}: "
              f"{t['amount']:,.2f} ({t['description']})")


def demo_validation():
    """
    Сценарий 2: Демонстрация валидации.
    Показывает работу валидации при создании и операциях.
    """
    print_separator("СЦЕНАРИЙ 2: ДЕМОНСТРАЦИЯ ВАЛИДАЦИИ")
    
    # 1. Валидация при создании
    print("\n❌ Попытка создания счета с некорректными данными:")
    
    test_cases = [
        ("", "RUB", 1000, "Пустое ФИО"),
        ("A", "RUB", 1000, "Слишком короткое ФИО"),
        ("Иван123", "RUB", 1000, "ФИО с цифрами"),
        ("Иванов Иван", "XYZ", 1000, "Неверная валюта"),
        ("Иванов Иван", "RUB", -1000, "Отрицательный баланс"),
        ("Иванов Иван", "RUB", 2_000_000_000, "Превышение максимального баланса"),
    ]
    
    for owner, currency, balance, description in test_cases:
        try:
            print(f"\n  Тест: {description}")
            account = BankAccount(owner, currency, balance)
            print(f"  ✅ Успех: {account}")
        except ValueError as e:
            print(f"  ❌ Ошибка: {e}")
    
    # 2. Валидация при операциях
    print("\n\n❌ Попытка выполнения некорректных операций:")
    account = BankAccount("Сидоров Сидор Сидорович", "RUB", 10000)
    print(f"\nСоздан счет: {account.owner_name}, баланс: {account.balance:,.2f} {account.currency}")
    
    # Попытка снять больше, чем есть
    try:
        print("\n  Попытка снять 15 000 (доступно 10 000):")
        account.withdraw(15000)
    except ValueError as e:
        print(f"  ❌ Ошибка: {e}")
    
    # Попытка пополнить с отрицательной суммой
    try:
        print("\n  Попытка пополнить на -5 000:")
        account.deposit(-5000)
    except ValueError as e:
        print(f"  ❌ Ошибка: {e}")
    
    # Попытка перевести в другой валюте
    try:
        print("\n  Попытка перевести на счет в другой валюте:")
        account_usd = BankAccount("Тестов Тест", "USD", 1000)
        account.transfer(account_usd, 5000)
    except ValueError as e:
        print(f"  ❌ Ошибка: {e}")


def demo_state_management():
    """
    Сценарий 3: Демонстрация логических состояний и изменения состояния.
    Показывает как состояние счета влияет на доступные операции.
    """
    print_separator("СЦЕНАРИЙ 3: УПРАВЛЕНИЕ СОСТОЯНИЕМ СЧЕТА")
    
    # Создаем счет
    account = BankAccount("Николаев Николай", "RUB", 50000)
    print("📝 Начальное состояние:")
    print(account)
    
    # Демонстрация изменения состояний
    states_demo = [
        ("Блокировка счета", account.block, []),
        ("Попытка снятия с заблокированного счета", account.withdraw, [1000]),
        ("Активация счета", account.activate, []),
        ("Снятие после активации", account.withdraw, [1000]),
        ("Заморозка счета", account.freeze, []),
        ("Пополнение замороженного счета", account.deposit, [5000]),
        ("Попытка снятия с замороженного счета", account.withdraw, [1000]),
        ("Закрытие счета (с положительным балансом)", account.close, []),
        ("Снятие всех средств", account.withdraw, [54000]),
        ("Закрытие счета", account.close, []),
        ("Попытка операции с закрытым счетом", account.deposit, [1000]),
    ]
    
    for description, method, args in states_demo:
        print(f"\n🔄 {description}:")
        print(f"   Текущий статус: {account.status.value}, баланс: {account.balance:,.2f}")
        
        try:
            if args:
                method(*args)
            else:
                method()
            print(f"   ✅ Успех. Новый статус: {account.status.value}, "
                  f"баланс: {account.balance:,.2f}")
        except ValueError as e:
            print(f"   ❌ Ошибка: {e}")
    
    print("\n📊 Итоговое состояние счета:")
    print(account)


def demo_magic_methods():
    """
    Сценарий 4: Демонстрация магических методов.
    Показывает работу __str__, __repr__, __eq__, __len__.
    """
    print_separator("СЦЕНАРИЙ 4: МАГИЧЕСКИЕ МЕТОДЫ")
    
    # Создаем счета
    acc1 = BankAccount("Алексеев Алексей", "RUB", 15000)
    acc2 = BankAccount("Алексеев Алексей", "RUB", 15000)  # Другой номер счета
    acc3 = BankAccount("Борисов Борис", "USD", 1000)
    
    print("📝 Созданы счета:")
    print(f"acc1: {repr(acc1)}")
    print(f"acc2: {repr(acc2)}")
    print(f"acc3: {repr(acc3)}")
    
    # Демонстрация __str__
    print("\n📌 __str__() - для пользователей:")
    print(acc1)
    
    # Демонстрация __repr__
    print("\n📌 __repr__() - для разработчиков:")
    print(f"repr(acc1) = {repr(acc1)}")
    
    # Демонстрация __eq__
    print("\n📌 __eq__() - сравнение счетов:")
    print(f"acc1 == acc2: {acc1 == acc2} (разные номера)")
    print(f"acc1 == acc1: {acc1 == acc1} (один и тот же объект)")
    print(f"acc1 == acc3: {acc1 == acc3} (разные счета)")
    print(f"acc1 == 'строка': {acc1 == 'строка'} (разные типы)")
    
    # Демонстрация __len__
    print("\n📌 __len__() - количество транзакций:")
    
    # Выполняем несколько операций
    acc1.deposit(5000, "Бонус")
    acc1.withdraw(2000, "Покупки")
    acc1.deposit(1000, "Кэшбэк")
    
    print(f"Количество транзакций по acc1: {len(acc1)}")
    print(f"Количество транзакций по acc2: {len(acc2)}")
    
    # Показываем транзакции
    print("\n📋 Транзакции acc1:")
    for i, t in enumerate(acc1.get_transaction_history(), 1):
        print(f"  {i}. {t['type']}: {t['amount']:>7,.2f} - {t['description']}")


def demo_class_attributes():
    """
    Сценарий 5: Демонстрация атрибутов класса.
    Показывает доступ к атрибутам класса через класс и экземпляр.
    """
    print_separator("СЦЕНАРИЙ 5: АТРИБУТЫ КЛАССА")
    
    print("📊 Атрибуты класса BankAccount:")
    print(f"  MAX_BALANCE (через класс): {BankAccount.MAX_BALANCE:,.0f}")
    print(f"  MIN_BALANCE (через класс): {BankAccount.MIN_BALANCE:,.0f}")
    print(f"  VALID_CURRENCIES (через класс): {BankAccount.VALID_CURRENCIES}")
    
    # Создаем счета
    acc1 = BankAccount("Владелец 1", "RUB")
    acc2 = BankAccount("Владелец 2", "USD")
    acc3 = BankAccount("Владелец 3", "EUR")
    
    print(f"\n📝 Создано {BankAccount._account_counter - 1000} счетов")
    
    print("\n📌 Доступ к атрибутам класса через экземпляры:")
    print(f"  acc1.MAX_BALANCE: {acc1.MAX_BALANCE:,.0f}")
    print(f"  acc2.MAX_BALANCE: {acc2.MAX_BALANCE:,.0f}")
    print(f"  acc3.MAX_BALANCE: {acc3.MAX_BALANCE:,.0f}")
    
    print("\n📌 Номера счетов (генерируются автоматически):")
    print(f"  acc1: {acc1.account_number}")
    print(f"  acc2: {acc2.account_number}")
    print(f"  acc3: {acc3.account_number}")
    
    # Демонстрация счетчика
    print(f"\n📌 Счетчик аккаунтов: {BankAccount._account_counter - 1000}")
    print(f"  (доступен только внутри класса, для внешнего кода скрыт)")


def main():
    """
    Главная функция, запускающая все сценарии демонстрации.
    """
    print("=" * 60)
    print("     ЛАБОРАТОРНАЯ РАБОТА №1: БАНКОВСКАЯ СИСТЕМА".center(60))
    print("=" * 60)
    print("\nВыполнил: Студент группы ...")
    print(f"Дата: {datetime.now().strftime('%d.%m.%Y %H:%M')}")
    
    # Запуск всех сценариев
    demo_creation_and_basic_operations()
    demo_validation()
    demo_state_management()
    demo_magic_methods()
    demo_class_attributes()
    
    print_separator("ИТОГ")
    print("""
✅ Реализовано:
   • Класс BankAccount с закрытыми атрибутами
   • Конструктор с проверкой входных данных
   • Свойства (@property) с геттерами и сеттерами
   • Методы валидации (_validate_*)
   • Методы изменения состояния (activate, block, freeze, close)
   • Поведение, зависящее от состояния
   • Бизнес-методы (deposit, withdraw, transfer)
   • Магические методы (__str__, __repr__, __eq__, __len__)
   • Атрибуты класса (MAX_BALANCE, MIN_BALANCE, VALID_CURRENCIES)
   • Демонстрация всех возможностей в 5 сценариях
    """)


if __name__ == "__main__":
    main()