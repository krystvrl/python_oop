"""
Модуль с валидаторами для банковских счетов.
Содержит функции валидации для переиспользования.
"""

from typing import Any
from enum import Enum


class AccountStatus(Enum):
    """Статусы банковского счета."""
    ACTIVE = "активен"
    BLOCKED = "заблокирован"
    CLOSED = "закрыт"
    FROZEN = "заморожен"


def validate_owner_name(name: str) -> bool:
    """
    Валидация ФИО владельца.
    
    Args:
        name: Проверяемое ФИО
        
    Returns:
        bool: True если валидация пройдена
        
    Raises:
        ValueError: Если ФИО некорректно
    """
    if not isinstance(name, str):
        raise ValueError("ФИО должно быть строкой")
    
    if not name or name.strip() == "":
        raise ValueError("ФИО не может быть пустым")
    
    if len(name.strip()) < 5:
        raise ValueError("ФИО должно содержать минимум 5 символов")
    
    if len(name.strip()) > 100:
        raise ValueError("ФИО должно содержать максимум 100 символов")
    
    # Проверка, что строка содержит только буквы, пробелы и дефисы
    if not all(c.isalpha() or c.isspace() or c == '-' for c in name.strip()):
        raise ValueError("ФИО может содержать только буквы, пробелы и дефис")
    
    return True


def validate_currency(currency: str, valid_currencies: list) -> bool:
    """
    Валидация валюты счета.
    
    Args:
        currency: Код валюты
        valid_currencies: Список допустимых валют
        
    Returns:
        bool: True если валидация пройдена
        
    Raises:
        ValueError: Если валюта некорректна
    """
    if not isinstance(currency, str):
        raise ValueError("Валюта должна быть строкой")
    
    if currency not in valid_currencies:
        raise ValueError(f"Валюта должна быть одной из: {', '.join(valid_currencies)}")
    
    return True


def validate_balance_limit(amount: float, current_balance: float, 
                           max_balance: float, currency: str) -> bool:
    """
    Валидация лимита баланса.
    
    Args:
        amount: Сумма для проверки
        current_balance: Текущий баланс
        max_balance: Максимальный допустимый баланс
        currency: Валюта счета
        
    Returns:
        bool: True если валидация пройдена
        
    Raises:
        ValueError: Если сумма некорректна
    """
    if not isinstance(amount, (int, float)):
        raise ValueError("Сумма должна быть числом")
    
    if amount < 0:
        raise ValueError("Сумма не может быть отрицательной")
    
    if current_balance + amount > max_balance:
        raise ValueError(f"Пополнение превысит максимальный баланс "
                       f"({max_balance:,.0f} {currency})")
    
    return True


def validate_withdrawal(amount: float, balance: float, status: AccountStatus) -> bool:
    """
    Валидация операции снятия средств.
    
    Args:
        amount: Сумма снятия
        balance: Текущий баланс
        status: Статус счета
        
    Returns:
        bool: True если валидация пройдена
        
    Raises:
        ValueError: Если операция невозможна
    """
    if status != AccountStatus.ACTIVE:
        raise ValueError(f"Невозможно снять средства. Счет {status.value}")
    
    if not isinstance(amount, (int, float)):
        raise ValueError("Сумма должна быть числом")
    
    if amount <= 0:
        raise ValueError("Сумма снятия должна быть положительной")
    
    if amount > balance:
        raise ValueError(f"Недостаточно средств. Доступно: {balance:.2f}")
    
    return True


def validate_deposit(amount: float, current_balance: float, 
                     status: AccountStatus, max_balance: float, 
                     currency: str) -> bool:
    """
    Валидация операции пополнения счета.
    
    Args:
        amount: Сумма пополнения
        current_balance: Текущий баланс
        status: Статус счета
        max_balance: Максимальный баланс
        currency: Валюта счета
        
    Returns:
        bool: True если валидация пройдена
        
    Raises:
        ValueError: Если операция невозможна
    """
    if status not in [AccountStatus.ACTIVE, AccountStatus.FROZEN]:
        raise ValueError(f"Невозможно пополнить счет. Счет {status.value}")
    
    if not isinstance(amount, (int, float)):
        raise ValueError("Сумма должна быть числом")
    
    if amount <= 0:
        raise ValueError("Сумма пополнения должна быть положительной")
    
    if current_balance + amount > max_balance:
        raise ValueError(f"Пополнение превысит максимальный баланс "
                       f"({max_balance:,.0f} {currency})")
    
    return True