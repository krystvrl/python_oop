"""
Модуль для работы с банковскими счетами.
Содержит класс BankAccount с использованием внешних валидаторов.
"""

from datetime import datetime, date
from typing import Optional, List
from validate import (
    AccountStatus,
    validate_owner_name,
    validate_currency,
    validate_balance_limit,
    validate_withdrawal,
    validate_deposit
)


class BankAccount:
    """Класс банковского счета."""
    
    # Атрибуты класса
    _account_counter = 1000
    MAX_BALANCE = 1_000_000_000.0  # Максимальный баланс (1 млрд)
    MIN_BALANCE = 0.0  # Минимальный баланс (для обычного счета)
    
    # Список допустимых валют
    VALID_CURRENCIES = ["RUB", "USD", "EUR", "GBP", "CNY"]
    
    def __init__(self, owner_name: str, currency: str = "RUB", 
                 initial_balance: float = 0.0):
        
        # Закрытые атрибуты экземпляра
        self.__account_number = f"40817810{BankAccount._account_counter}"
        BankAccount._account_counter += 1
        
        self.__owner_name = ""
        self.__balance = 0.0
        self.__currency = ""
        self.__status = AccountStatus.ACTIVE
        self.__created_date = date.today()
        self.__transactions = []
        
        # Установка значений через свойства с валидацией
        self.owner_name = owner_name
        self.currency = currency
        
        # Установка начального баланса с валидацией
        if initial_balance > 0:
            self.deposit(initial_balance, "Начальный взнос")
    
    # Свойства (геттеры и сеттеры)
    
    @property
    def account_number(self) -> str:
        """Геттер для номера счета (только чтение)."""
        return self.__account_number
    
    @property
    def owner_name(self) -> str:
        """Геттер для ФИО владельца."""
        return self.__owner_name
    
    @owner_name.setter
    def owner_name(self, value: str):
        """Сеттер для ФИО владельца с валидацией."""
        validate_owner_name(value)
        self.__owner_name = value.strip()
    
    @property
    def balance(self) -> float:
        """Геттер для баланса (только чтение)."""
        return self.__balance
    
    @property
    def currency(self) -> str:
        """Геттер для валюты счета."""
        return self.__currency
    
    @currency.setter
    def currency(self, value: str):
        """Сеттер для валюты счета с валидацией."""
        validate_currency(value, BankAccount.VALID_CURRENCIES)
        self.__currency = value
    
    @property
    def status(self) -> AccountStatus:
        """Геттер для статуса счета (только чтение)."""
        return self.__status
    
    @property
    def created_date(self) -> date:
        """Геттер для даты открытия (только чтение)."""
        return self.__created_date
    
    @property
    def transaction_count(self) -> int:
        """Геттер для количества транзакций."""
        return len(self.__transactions)
    
    # Методы изменения состояния
    
    def activate(self) -> None:
        """Активация счета."""
        if self.__status == AccountStatus.CLOSED:
            raise ValueError("Нельзя активировать закрытый счет")
        self.__status = AccountStatus.ACTIVE
        self.__add_transaction("INFO", 0, "Счет активирован")
    
    def block(self) -> None:
        """Блокировка счета."""
        if self.__status == AccountStatus.CLOSED:
            raise ValueError("Нельзя заблокировать закрытый счет")
        self.__status = AccountStatus.BLOCKED
        self.__add_transaction("INFO", 0, "Счет заблокирован")
    
    def freeze(self) -> None:
        """Заморозка счета (только пополнение)."""
        if self.__status == AccountStatus.CLOSED:
            raise ValueError("Нельзя заморозить закрытый счет")
        self.__status = AccountStatus.FROZEN
        self.__add_transaction("INFO", 0, "Счет заморожен")
    
    def close(self) -> None:
        """Закрытие счета."""
        if self.__balance > 0:
            raise ValueError(f"Невозможно закрыть счет с положительным балансом: "
                           f"{self.__balance:.2f} {self.__currency}")
        
        if self.__balance < 0:
            raise ValueError(f"Невозможно закрыть счет с отрицательным балансом: "
                           f"{self.__balance:.2f} {self.__currency}")
        
        self.__status = AccountStatus.CLOSED
        self.__add_transaction("INFO", 0, "Счет закрыт")
    
    # Бизнес-методы
    
    def deposit(self, amount: float, description: str = "Пополнение счета") -> dict:
        """Пополнение счета."""
        # Валидация операции (поведение, зависящее от состояния)
        validate_deposit(amount, self.__balance, self.__status, 
                        BankAccount.MAX_BALANCE, self.__currency)
        
        # Выполнение операции
        self.__balance += amount
        
        # Запись транзакции
        transaction = self.__add_transaction("DEPOSIT", amount, description)
        
        return transaction
    
    def withdraw(self, amount: float, description: str = "Снятие со счета") -> dict:
        """Снятие средств со счета."""
        # Валидация операции (поведение, зависящее от состояния)
        validate_withdrawal(amount, self.__balance, self.__status)
        
        # Выполнение операции
        self.__balance -= amount
        
        # Запись транзакции
        transaction = self.__add_transaction("WITHDRAWAL", amount, description)
        
        return transaction
    
    def transfer(self, to_account: 'BankAccount', amount: float, 
                 description: str = "Перевод") -> dict:
        """Перевод средств на другой счет."""
        if not isinstance(to_account, BankAccount):
            raise ValueError("Получатель должен быть банковским счетом")
        
        if self.__currency != to_account.__currency:
            raise ValueError(f"Невозможно выполнить перевод. Валюты счетов различаются: "
                           f"{self.__currency} и {to_account.__currency}")
        
        # Снятие со своего счета
        self.withdraw(amount, f"Перевод: {description}")
        
        # Пополнение счета получателя
        to_account.deposit(amount, f"Перевод: {description}")
        
        # Запись транзакции перевода
        transaction = {
            "type": "TRANSFER",
            "amount": amount,
            "from": self.__account_number,
            "to": to_account.__account_number,
            "description": description,
            "date": datetime.now(),
            "balance_after": self.__balance
        }
        
        return transaction
    
    def get_transaction_history(self, limit: Optional[int] = None) -> List[dict]:
        """Получение истории транзакций."""
        if limit:
            return self.__transactions[-limit:]
        return self.__transactions.copy()
    
    def get_account_info(self) -> dict:
        """Получение полной информации о счете."""
        return {
            "account_number": self.__account_number,
            "owner_name": self.__owner_name,
            "balance": self.__balance,
            "currency": self.__currency,
            "status": self.__status.value,
            "created_date": self.__created_date.strftime("%d.%m.%Y"),
            "transactions": self.transaction_count
        }
    
    # Вспомогательные методы
    
    def __add_transaction(self, transaction_type: str, amount: float, 
                          description: str) -> dict:
        """Добавление транзакции в историю."""
        transaction = {
            "type": transaction_type,
            "amount": amount,
            "description": description,
            "date": datetime.now(),
            "balance_after": self.__balance
        }
        self.__transactions.append(transaction)
        return transaction
    
    # Магические методы
    
    def __str__(self) -> str:
        """Строковое представление счета."""
        return (f"🏦 Счет {self.__account_number}\n"
                f"   Владелец: {self.__owner_name}\n"
                f"   Баланс: {self.__balance:>15,.2f} {self.__currency}\n"
                f"   Статус: {self.__status.value}\n"
                f"   Открыт: {self.__created_date.strftime('%d.%m.%Y')}")
    
    def __repr__(self) -> str:
        """Представление для отладки."""
        return (f"BankAccount(owner_name='{self.__owner_name}', "
                f"currency='{self.__currency}', "
                f"balance={self.__balance:.2f}, "
                f"status='{self.__status.value}')")
    
    def __eq__(self, other: object) -> bool:
        """Сравнение счетов по номеру."""
        if not isinstance(other, BankAccount):
            return False
        return self.__account_number == other.__account_number
    
    def __len__(self) -> int:
        """Возвращает количество транзакций."""
        return len(self.__transactions)