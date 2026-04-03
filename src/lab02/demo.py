from model import BankAccount
from collection import BankAccountCollection
from validate import AccountStatus


def print_separator(title: str = ""):
    """Вывод разделителя с заголовком."""
    print("\n" + "=" * 60)
    if title:
        print(f"  {title}")
        print("=" * 60)
    else:
        print("=" * 60)


def print_collection_info(collection: BankAccountCollection, name: str = "Коллекция"):
    """Вывод информации о коллекции."""
    print(f"\n{name}:")
    print(f"  Размер: {len(collection)}")
    if len(collection) > 0:
        print(f"  Общий баланс: {collection.total_balance():,.2f}")
        print(f"  Средний баланс: {collection.average_balance():,.2f}")
        print("\n  Содержимое:")
        for i, account in enumerate(collection, 1):
            print(f"    {i}. {account.account_number} | {account.owner_name} | "
                  f"{account.balance:,.2f} {account.currency} | {account.status.value}")


def scenario_1_basic_operations():
    """Сценарий 1: Базовые операции с коллекцией."""
    print_separator("СЦЕНАРИЙ 1: Базовые операции (добавление, удаление, поиск)")
    
    # Создание коллекции
    collection = BankAccountCollection()
    print("\n✓ Создана пустая коллекция")
    
    # Создание счетов
    acc1 = BankAccount("Маленкова Мария Андреевна", "RUB", 100000)
    acc2 = BankAccount("Петров Алексей Юрьевич", "USD", 5000)
    acc3 = BankAccount("Сидорова Виолетта Олеговна", "EUR", 3000)
    acc4 = BankAccount("Козлов Дмитрий Анатольевич", "RUB", 250000)
    
    print("\n✓ Созданы счета:")
    print(f"  1. {acc1.account_number} - {acc1.owner_name} ({acc1.balance:.2f} {acc1.currency})")
    print(f"  2. {acc2.account_number} - {acc2.owner_name} ({acc2.balance:.2f} {acc2.currency})")
    print(f"  3. {acc3.account_number} - {acc3.owner_name} ({acc3.balance:.2f} {acc3.currency})")
    print(f"  4. {acc4.account_number} - {acc4.owner_name} ({acc4.balance:.2f} {acc4.currency})")
    
    # Добавление в коллекцию
    collection.add(acc1)
    collection.add(acc2)
    collection.add(acc3)
    collection.add(acc4)
    print("\n✓ Все счета добавлены в коллекцию")
    
    # Попытка добавить дубликат
    try:
        collection.add(acc1)
        print("❌ Ошибка: дубликат был добавлен!")
    except ValueError as e:
        print(f"✓ Проверка дубликатов работает: {e}")
    
    # Попытка добавить объект неправильного типа
    try:
        collection.add("not a bank account")
        print("❌ Ошибка: неправильный тип был добавлен!")
    except TypeError as e:
        print(f"✓ Проверка типа работает: {e}")
    
    # Вывод коллекции
    print_collection_info(collection, "Текущая коллекция")
    
    # Поиск по номеру счета
    found = collection.find_by_account_number(acc2.account_number)
    if found:
        print(f"\n✓ Поиск по номеру {acc2.account_number}: найден счет {found.owner_name}")
    
    # Поиск по ФИО
    found_names = collection.find_by_owner_name("Маленкова")
    print(f"\n✓ Поиск по ФИО 'Маленкова': найдено {len(found_names)} счет(ов)")
    for acc in found_names:
        print(f"   - {acc.owner_name} ({acc.account_number})")
    
    # Удаление счета
    collection.remove(acc3)
    print(f"\n✓ Удален счет {acc3.account_number} ({acc3.owner_name})")
    print_collection_info(collection, "Коллекция после удаления")


def scenario_2_iteration_and_indexing():
    """Сценарий 2: Итерация и индексация."""
    print_separator("СЦЕНАРИЙ 2: Итерация по коллекции и индексация")
    
    # Создание коллекции
    collection = BankAccountCollection()
    
    # Добавление нескольких счетов
    accounts_data = [
        ("Линник Мария Рустамовна", "RUB", 150000),
        ("Мишустин Богдан Сергеевич", "USD", 10000),
        ("Борисова Зинаида Тимофеевна", "EUR", 7500),
        ("Федоров Александр Игоревич", "RUB", 50000),
        ("Новикова Зоя Павловна", "RUB", 320000),
    ]
    
    for name, currency, balance in accounts_data:
        account = BankAccount(name, currency, balance)
        collection.add(account)
    
    print("\n✓ Создана коллекция из 5 счетов")
    
    # Итерация с помощью for
    print("\n1. Итерация с помощью 'for account in collection':")
    for i, account in enumerate(collection, 1):
        print(f"   {i}. {account.owner_name:30} | {account.balance:>10,.2f} {account.currency}")
    
    # Использование len()
    print(f"\n2. Использование len(): в коллекции {len(collection)} счетов")
    
    # Индексация
    print("\n3. Индексация collection[index]:")
    print(f"   collection[0] = {collection[0].owner_name} ({collection[0].account_number})")
    print(f"   collection[2] = {collection[2].owner_name} ({collection[2].account_number})")
    print(f"   collection[-1] = {collection[-1].owner_name} ({collection[-1].account_number})")
    
    # Удаление по индексу
    removed = collection.remove_at(2)
    print(f"\n4. Удаление по индексу: удален '{removed.owner_name}'")
    print_collection_info(collection, "Коллекция после удаления по индексу")
    
    # Срезы
    print("\n5. Использование срезов collection[1:4]:")
    sliced = collection[1:4]
    print(f"   Тип результата: {type(sliced).__name__}")
    print(f"   Размер среза: {len(sliced)}")
    for account in sliced:
        print(f"   - {account.owner_name}")


def scenario_3_sorting_and_filtering():
    """Сценарий 3: Сортировка и фильтрация."""
    print_separator("СЦЕНАРИЙ 3: Сортировка и фильтрация")
    
    # Создание коллекции
    collection = BankAccountCollection()
    
    # Добавление счетов с разными балансами и статусами
    acc1 = BankAccount("Платонов Сергей Владимирович", "RUB", 500000)
    acc2 = BankAccount("Трунова Василиса Алексеевна", "RUB", 25000)
    acc3 = BankAccount("Рощин Арсений Романович", "USD", 8000)
    acc4 = BankAccount("Елагина Наталья Сергеевна", "EUR", 12000)
    acc5 = BankAccount("Данилин Максим Семенович", "RUB", 75000)
    
    collection.add(acc1)
    collection.add(acc2)
    collection.add(acc3)
    collection.add(acc4)
    collection.add(acc5)
    
    # Блокируем один счет для демонстрации фильтрации
    acc2.block()
    
    print("\n✓ Создана коллекция из 5 счетов (один заблокирован)")
    
    # Сортировка по ФИО
    print("\n1. Сортировка по ФИО (по возрастанию):")
    collection.sort_by_owner_name()
    for account in collection:
        print(f"   - {account.owner_name:35} | {account.balance:>10,.2f} {account.currency}")
    
    # Сортировка по балансу
    print("\n2. Сортировка по балансу (по убыванию):")
    collection.sort_by_balance(reverse=True)
    for account in collection:
        print(f"   - {account.owner_name:35} | {account.balance:>10,.2f} {account.currency}")
    
    # Фильтрация: активные счета
    print("\n3. Фильтрация: get_active_accounts()")
    active = collection.get_active_accounts()
    print(f"   Активных счетов: {len(active)} из {len(collection)}")
    for account in active:
        print(f"   - {account.owner_name} | {account.status.value}")
    
    # Фильтрация: счета с положительным балансом
    print("\n4. Фильтрация: get_positive_balance_accounts()")
    positive = collection.get_positive_balance_accounts()
    print(f"   Счетов с положительным балансом: {len(positive)}")
    
    # Фильтрация по валюте
    print("\n5. Фильтрация: get_by_currency('RUB')")
    rub_accounts = collection.get_by_currency("RUB")
    print(f"   Счетов в RUB: {len(rub_accounts)}")
    for account in rub_accounts:
        print(f"   - {account.owner_name} | {account.balance:.2f} {account.currency}")
    
    # Универсальная фильтрация
    print("\n6. Универсальная фильтрация: счета с балансом > 100 000")
    large_balances = collection.get_filtered(lambda acc: acc.balance > 100000)
    print(f"   Счетов с балансом > 100 000: {len(large_balances)}")
    for account in large_balances:
        print(f"   - {account.owner_name} | {account.balance:,.2f} {account.currency}")
    
    # Статистика
    print("\n7. Статистика коллекции:")
    print(f"   Общий баланс: {collection.total_balance():,.2f}")
    print(f"   Средний баланс: {collection.average_balance():,.2f}")
    print(f"   Активных счетов: {collection.count_by_status(AccountStatus.ACTIVE)}")
    print(f"   Заблокированных: {collection.count_by_status(AccountStatus.BLOCKED)}")


def scenario_4_transfer_and_business_logic():
    """Сценарий 4: Переводы и бизнес-логика."""
    print_separator("СЦЕНАРИЙ 4: Банковские операции и транзакции")
    
    # Создание коллекции
    collection = BankAccountCollection()
    
    # Создание счетов для перевода
    acc_from = BankAccount("Отправитель Владимир Шиндин", "RUB", 100000)
    acc_to = BankAccount("Получатель Константин Просолов", "RUB", 50000)
    
    collection.add(acc_from)
    collection.add(acc_to)
    
    print("\n✓ Созданы счета для перевода:")
    print(f"   Счет отправителя: {acc_from.account_number}")
    print(f"     Баланс: {acc_from.balance:.2f} {acc_from.currency}")
    print(f"   Счет получателя: {acc_to.account_number}")
    print(f"     Баланс: {acc_to.balance:.2f} {acc_to.currency}")
    
    # Выполнение перевода
    amount = 25000
    print(f"\n✓ Выполняется перевод {amount:.2f} RUB...")
    acc_from.transfer(acc_to, amount, "Оплата услуг")
    
    print(f"\n✓ Перевод выполнен:")
    print(f"   Баланс отправителя: {acc_from.balance:.2f} RUB")
    print(f"   Баланс получателя: {acc_to.balance:.2f} RUB")
    
    # История транзакций
    print(f"\n✓ История транзакций отправителя (последние 3):")
    for tx in acc_from.get_transaction_history(3):
        print(f"   - {tx['type']}: {tx['amount']:.2f} | {tx['description']}")
    
    # Пополнение счета
    print(f"\n✓ Пополнение счета отправителя на 10000 RUB...")
    acc_from.deposit(10000, "Зарплата")
    print(f"   Новый баланс: {acc_from.balance:.2f} RUB")
    
    # Информация о счете
    print("\n✓ Полная информация о счете отправителя:")
    info = acc_from.get_account_info()
    for key, value in info.items():
        print(f"   {key}: {value}")


def main():
    """Основная функция демонстрации."""
    print("\n" + "=" * 60)
    print("   ЛАБОРАТОРНАЯ РАБОТА №2")
    print("   КОЛЛЕКЦИЯ БАНКОВСКИХ СЧЕТОВ")
    print("=" * 60)
    
    # Запуск всех сценариев
    scenario_1_basic_operations()
    scenario_2_iteration_and_indexing()
    scenario_3_sorting_and_filtering()
    scenario_4_transfer_and_business_logic()
    
if __name__ == "__main__":
    main()