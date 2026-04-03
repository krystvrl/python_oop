from typing import List, Optional, Callable, Any
from copy import deepcopy
from model import BankAccount


class BankAccountCollection:
    """
    Коллекция для хранения и управления банковскими счетами.
    Реализует все необходимые методы для работы с коллекцией.
    """
    
    def __init__(self):
        """Инициализация пустой коллекции."""
        self._items: List[BankAccount] = []
    
    # Базовые методы управления коллекцией
    
    def add(self, item: BankAccount) -> None:
        if not isinstance(item, BankAccount):
            raise TypeError(f"Можно добавлять только объекты BankAccount. "
                          f"Получен {type(item).__name__}")
        
        # Проверка на дубликаты по номеру счета
        if self.contains(item):
            raise ValueError(f"Счет {item.account_number} уже существует в коллекции")
        
        self._items.append(item)
    
    def remove(self, item: BankAccount) -> bool:
        try:
            self._items.remove(item)
            return True
        except ValueError:
            return False
    
    def remove_at(self, index: int) -> BankAccount:
        if not isinstance(index, int):
            raise TypeError("Индекс должен быть целым числом")
        
        if index < 0 or index >= len(self._items):
            raise IndexError(f"Индекс {index} вне диапазона [0, {len(self._items) - 1}]")
        
        return self._items.pop(index)
    
    def get_all(self) -> List[BankAccount]:
        """
        Возвращает копию списка всех объектов.
        
        Returns:
            List[BankAccount]: Копия списка счетов
        """
        return self._items.copy()
    
    def get_by_index(self, index: int) -> BankAccount:
        if not isinstance(index, int):
            raise TypeError("Индекс должен быть целым числом")
        
        if index < 0 or index >= len(self._items):
            raise IndexError(f"Индекс {index} вне диапазона [0, {len(self._items) - 1}]")
        
        return self._items[index]
    
    def contains(self, item: BankAccount) -> bool:
        """
        Проверка наличия объекта в коллекции.
        """
        return item in self._items
    
    def clear(self) -> None:
        """Очистка коллекции."""
        self._items.clear()
    
    # Методы поиска
    
    def find_by_account_number(self, account_number: str) -> Optional[BankAccount]:
        """
        Поиск счета по номеру.
        """
        for item in self._items:
            if item.account_number == account_number:
                return item
        return None
    
    def find_by_owner_name(self, owner_name: str) -> List[BankAccount]:
        """
        Поиск счетов по ФИО владельца (частичное совпадение).
        """
        result = []
        search_name = owner_name.lower()
        for item in self._items:
            if search_name in item.owner_name.lower():
                result.append(item)
        return result
    
    def find_by_status(self, status) -> List[BankAccount]:
        """
        Поиск счетов по статусу.
        """
        result = []
        for item in self._items:
            if item.status == status:
                result.append(item)
        return result
    
    def find_by_min_balance(self, min_balance: float) -> List[BankAccount]:
        """
        Поиск счетов с балансом не менее указанного.
        """
        return [item for item in self._items if item.balance >= min_balance]
    
    def find_by_currency(self, currency: str) -> List[BankAccount]:
        """
        Поиск счетов по валюте.
        """
        return [item for item in self._items if item.currency == currency.upper()]
    
    # Методы сортировки
    
    def sort_by_owner_name(self, reverse: bool = False) -> None:
        """
        Сортировка коллекции по ФИО владельца.
       
            reverse: Если True, сортировка в обратном порядке
        """
        self._items.sort(key=lambda acc: acc.owner_name, reverse=reverse)
    
    def sort_by_balance(self, reverse: bool = False) -> None:
        """
        Сортировка коллекции по балансу.

            reverse: Если True, сортировка в обратном порядке
        """
        self._items.sort(key=lambda acc: acc.balance, reverse=reverse)
    
    def sort_by_account_number(self, reverse: bool = False) -> None:
        """
        Сортировка коллекции по номеру счета.
        """
        self._items.sort(key=lambda acc: acc.account_number, reverse=reverse)
    
    def sort_by_created_date(self, reverse: bool = False) -> None:
        """
        Сортировка коллекции по дате создания.
        """
        self._items.sort(key=lambda acc: acc.created_date, reverse=reverse)
    
    def sort(self, key: Optional[Callable[[BankAccount], Any]] = None, 
             reverse: bool = False) -> None:
        """
        Универсальная сортировка коллекции.
            key: Функция для получения ключа сортировки
        """
        if key is None:
            self._items.sort(reverse=reverse)
        else:
            self._items.sort(key=key, reverse=reverse)
    
    # Методы фильтрации (возвращают новые коллекции)
    
    def get_active_accounts(self) -> 'BankAccountCollection':
        """
        Получение всех активных счетов.
        
        Returns:
            BankAccountCollection: Новая коллекция с активными счетами
        """
        from validate import AccountStatus
        
        new_collection = BankAccountCollection()
        for item in self._items:
            if item.status == AccountStatus.ACTIVE:
                new_collection.add(item)
        return new_collection
    
    def get_positive_balance_accounts(self) -> 'BankAccountCollection':
        """
        Получение счетов с положительным балансом.
        
        Returns:
            BankAccountCollection: Новая коллекция счетов с положительным балансом
        """
        new_collection = BankAccountCollection()
        for item in self._items:
            if item.balance > 0:
                new_collection.add(item)
        return new_collection
    
    def get_by_currency(self, currency: str) -> 'BankAccountCollection':
        """
        Получение счетов в указанной валюте.
        """
        new_collection = BankAccountCollection()
        for item in self._items:
            if item.currency == currency.upper():
                new_collection.add(item)
        return new_collection
    
    def get_filtered(self, predicate: Callable[[BankAccount], bool]) -> 'BankAccountCollection':
        """
        Универсальная фильтрация коллекции.
        
        Args:
            predicate: Функция-предикат для фильтрации
            
        Returns:
            BankAccountCollection: Новая отфильтрованная коллекция
        """
        new_collection = BankAccountCollection()
        for item in self._items:
            if predicate(item):
                new_collection.add(item)
        return new_collection
    
    # Статистические методы
    
    def total_balance(self) -> float:
        """
        Суммарный баланс всех счетов.
        
        Returns:
            float: Общая сумма на всех счетах
        """
        return sum(item.balance for item in self._items)
    
    def average_balance(self) -> float:
        """
        Средний баланс по всем счетам.
        
        Returns:
            float: Средний баланс
        """
        if not self._items:
            return 0.0
        return self.total_balance() / len(self._items)
    
    def count_by_status(self, status) -> int:
        """
        Подсчет счетов с определенным статусом.
            
        Returns:
            int: Количество счетов
        """
        return sum(1 for item in self._items if item.status == status)
    
    # Магические методы
    
    def __len__(self) -> int:
        """
        Возвращает количество элементов в коллекции.
        
        Returns:
            int: Размер коллекции
        """
        return len(self._items)
    
    def __getitem__(self, index: int) -> BankAccount:
        """
        Поддержка индексации коллекции.
        
        Args:
            index: Индекс элемента
            
        Raises:
            IndexError: Если индекс вне диапазона
        """
        if isinstance(index, slice):
            # Поддержка срезов
            new_collection = BankAccountCollection()
            for item in self._items[index]:
                new_collection.add(item)
            return new_collection
        
        if not isinstance(index, int):
            raise TypeError("Индекс должен быть целым числом")
        
        if index < 0:
            index = len(self._items) + index
        
        if index < 0 or index >= len(self._items):
            raise IndexError(f"Индекс {index} вне диапазона [0, {len(self._items) - 1}]")
        
        return self._items[index]
    
    def __iter__(self):
        """
        Поддержка итерации по коллекции.
        
        Returns:
            Iterator: Итератор по элементам коллекции
        """
        return iter(self._items)
    
    def __contains__(self, item: BankAccount) -> bool:
        """
        Поддержка оператора 'in'.
        
        Args:
            item: Проверяемый объект
            
        Returns:
            bool: True если объект в коллекции
        """
        return self.contains(item)
    
    def __str__(self) -> str:
        """Строковое представление коллекции."""
        if not self._items:
            return "BankAccountCollection (пустая)"
        
        result = f"BankAccountCollection (всего счетов: {len(self._items)})\n"
        result += "-" * 50 + "\n"
        for i, account in enumerate(self._items, 1):
            result += f"{i}. {account.account_number} | {account.owner_name} | "
            result += f"{account.balance:.2f} {account.currency} | {account.status.value}\n"
        return result
    
    def __repr__(self) -> str:
        """Представление для отладки."""
        return f"BankAccountCollection(items={repr(self._items)})"