"""
Модуль для работы с банковскими счетами.
Содержит базовый класс BankAccount.
"""

from datetime import datetime, date
from typing import Optional, List
from enum import Enum


class AccountStatus(Enum):
    """Статусы банковского счета."""
    ACTIVE = "активен"
    BLOCKED = "заблокирован"
    FROZEN = "заморожен"
    CLOSED = "закрыт"


def validate_owner_name(name: str) -> None:
    """Проверка ФИО владельца."""
    if not name or not isinstance(name, str):
        raise ValueError("ФИО владельца не может быть пустым")
    if len(name.strip()) < 3:
        raise ValueError("ФИО должно содержать минимум 3 символа")


def validate_currency(currency: str, valid_currencies: List[str]) -> None:
    """Проверка валюты."""
    if currency not in valid_currencies:
        raise ValueError(f"Валюта {currency} не поддерживается. "
                        f"Допустимые валюты: {valid_currencies}")


def validate_deposit(amount: float, balance: float, status: AccountStatus,
                     max_balance: float, currency: str) -> None:
    """Проверка операции пополнения."""
    if amount <= 0:
        raise ValueError(f"Сумма пополнения должна быть положительной: {amount}")
    if balance + amount > max_balance:
        raise ValueError(f"Превышение максимального баланса. "
                        f"Максимум: {max_balance:.2f} {currency}")
    if status == AccountStatus.BLOCKED:
        raise ValueError("Счет заблокирован. Операция невозможна")
    if status == AccountStatus.CLOSED:
        raise ValueError("Счет закрыт. Операция невозможна")


def validate_withdrawal(amount: float, balance: float, status: AccountStatus) -> None:
    """Проверка операции снятия."""
    if amount <= 0:
        raise ValueError(f"Сумма снятия должна быть положительной: {amount}")
    if amount > balance:
        raise ValueError(f"Недостаточно средств. Доступно: {balance:.2f}")
    if status == AccountStatus.BLOCKED:
        raise ValueError("Счет заблокирован. Операция невозможна")
    if status == AccountStatus.CLOSED:
        raise ValueError("Счет закрыт. Операция невозможна")


class BankAccount:
    """Базовый класс банковского счета."""
    
    _account_counter = 1000
    MAX_BALANCE = 1_000_000_000.0
    VALID_CURRENCIES = ["RUB", "USD", "EUR", "GBP", "CNY"]
    
    def __init__(self, owner_name: str, currency: str = "RUB", 
                 initial_balance: float = 0.0):
        
        self.__account_number = f"40817810{BankAccount._account_counter}"
        BankAccount._account_counter += 1
        
        self.__owner_name = ""
        self.__balance = 0.0
        self.__currency = ""
        self.__status = AccountStatus.ACTIVE
        self.__created_date = date.today()
        self.__transactions: List[dict] = []
        
        self.owner_name = owner_name
        self.currency = currency
        
        if initial_balance > 0:
            self.deposit(initial_balance, "Начальный взнос")
    
    @property
    def account_number(self) -> str:
        return self.__account_number
    
    @property
    def owner_name(self) -> str:
        return self.__owner_name
    
    @owner_name.setter
    def owner_name(self, value: str):
        validate_owner_name(value)
        self.__owner_name = value.strip()
    
    @property
    def balance(self) -> float:
        return self.__balance
    
    @property
    def currency(self) -> str:
        return self.__currency
    
    @currency.setter
    def currency(self, value: str):
        validate_currency(value, BankAccount.VALID_CURRENCIES)
        self.__currency = value
    
    @property
    def status(self) -> AccountStatus:
        return self.__status
    
    @property
    def created_date(self) -> date:
        return self.__created_date
    
    @property
    def transaction_count(self) -> int:
        return len(self.__transactions)
    
    def activate(self) -> None:
        if self.__status == AccountStatus.CLOSED:
            raise ValueError("Нельзя активировать закрытый счет")
        self.__status = AccountStatus.ACTIVE
        self._add_transaction("INFO", 0, "Счет активирован")
    
    def block(self) -> None:
        if self.__status == AccountStatus.CLOSED:
            raise ValueError("Нельзя заблокировать закрытый счет")
        self.__status = AccountStatus.BLOCKED
        self._add_transaction("INFO", 0, "Счет заблокирован")
    
    def freeze(self) -> None:
        if self.__status == AccountStatus.CLOSED:
            raise ValueError("Нельзя заморозить закрытый счет")
        self.__status = AccountStatus.FROZEN
        self._add_transaction("INFO", 0, "Счет заморожен")
    
    def close(self) -> None:
        if self.__balance > 0:
            raise ValueError("Невозможно закрыть счет с положительным балансом")
        if self.__balance < 0:
            raise ValueError("Невозможно закрыть счет с отрицательным балансом")
        self.__status = AccountStatus.CLOSED
        self._add_transaction("INFO", 0, "Счет закрыт")
    
    def deposit(self, amount: float, description: str = "Пополнение счета") -> dict:
        validate_deposit(amount, self.__balance, self.__status, 
                        BankAccount.MAX_BALANCE, self.__currency)
        self.__balance += amount
        return self._add_transaction("DEPOSIT", amount, description)
    
    def withdraw(self, amount: float, description: str = "Снятие со счета") -> dict:
        validate_withdrawal(amount, self.__balance, self.__status)
        self.__balance -= amount
        return self._add_transaction("WITHDRAWAL", amount, description)
    
    def transfer(self, to_account: 'BankAccount', amount: float, 
                 description: str = "Перевод") -> dict:
        if not isinstance(to_account, BankAccount):
            raise ValueError("Получатель должен быть банковским счетом")
        if self.__currency != to_account.__currency:
            raise ValueError("Валюты счетов различаются")
        
        self.withdraw(amount, f"Перевод: {description}")
        to_account.deposit(amount, f"Перевод: {description}")
        
        return {
            "type": "TRANSFER",
            "amount": amount,
            "from": self.__account_number,
            "to": to_account.__account_number,
            "description": description,
            "date": datetime.now(),
            "balance_after": self.__balance
        }
    
    def get_transaction_history(self, limit: Optional[int] = None) -> List[dict]:
        if limit:
            return self.__transactions[-limit:]
        return self.__transactions.copy()
    
    def get_account_info(self) -> dict:
        return {
            "account_number": self.__account_number,
            "owner_name": self.__owner_name,
            "balance": self.__balance,
            "currency": self.__currency,
            "status": self.__status.value,
            "created_date": self.__created_date.strftime("%d.%m.%Y"),
            "transactions": self.transaction_count
        }
    
    def calculate_annual_interest(self) -> float:
        """
        Расчет годового дохода по счету.
        Базовый метод (переопределяется в дочерних классах).
        """
        return 0.0

    def calculate_annual_income(self) -> float:
        """Совместимый алиас для старого названия метода."""
        return self.calculate_annual_interest()
    
    def _add_transaction(self, transaction_type: str, amount: float, 
                          description: str) -> dict:
        transaction = {
            "type": transaction_type,
            "amount": amount,
            "description": description,
            "date": datetime.now(),
            "balance_after": self.__balance
        }
        self.__transactions.append(transaction)
        return transaction
    
    def __str__(self) -> str:
        return (f"🏦 Счет {self.__account_number}\n"
                f"   Владелец: {self.__owner_name}\n"
                f"   Баланс: {self.__balance:>15,.2f} {self.__currency}\n"
                f"   Статус: {self.__status.value}\n"
                f"   Открыт: {self.__created_date.strftime('%d.%m.%Y')}")
    
    def __repr__(self) -> str:
        return (f"BankAccount(owner_name='{self.__owner_name}', "
                f"currency='{self.__currency}', "
                f"balance={self.__balance:.2f})")
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BankAccount):
            return False
        return self.__account_number == other.__account_number