"""
Пользовательские исключения для приложения управления банковскими счетами.
"""


class BankAppException(Exception):
    """Базовое исключение приложения."""
    pass


class AccountNotFoundError(BankAppException):
    """Счет не найден в коллекции."""
    pass


class DuplicateAccountError(BankAppException):
    """Счет с таким номером уже существует."""
    pass


class InvalidAccountTypeError(BankAppException):
    """Неверный тип счета."""
    pass


class InsufficientFundsError(BankAppException):
    """Недостаточно средств на счете."""
    pass


class OperationError(BankAppException):
    """Ошибка при выполнении операции."""
    pass


class StorageError(BankAppException):
    """Ошибка при работе с хранилищем данных."""
    pass

