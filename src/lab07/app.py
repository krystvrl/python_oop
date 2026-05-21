"""
Бизнес-логика приложения управления банковскими счетами.
"""

import sys
from pathlib import Path
from typing import List, Optional, Callable

# Настройка путей
def _ensure_paths() -> None:
    src_dir = Path(__file__).resolve().parents[1]
    if str(src_dir) not in sys.path:
        sys.path.insert(0, str(src_dir))
    lab03_dir = src_dir / "lab03"
    if str(lab03_dir) not in sys.path:
        sys.path.insert(0, str(lab03_dir))

_ensure_paths()

from lab03.base import BankAccount, AccountStatus
from lab03.models import SavingsAccount, CreditAccount
from lab05.strategies import by_owner_name, by_balance
from exceptions import (
    AccountNotFoundError, DuplicateAccountError, OperationError,
    InvalidAccountTypeError
)


class BankApp:
    """Основное приложение для управления банковскими счетами."""

    def __init__(self) -> None:
        """Инициализация приложения."""
        self._accounts: List[BankAccount] = []

    def add_account(self, account: BankAccount) -> None:
        """
        Добавить новый счет в коллекцию.
        Args:
            account: Объект банковского счета
        Raises:
            DuplicateAccountError: Если счет с таким номером уже существует
        """
        if self._find_by_number(account.account_number):
            raise DuplicateAccountError(
                f"Счет {account.account_number} уже существует"
            )
        self._accounts.append(account)

    def get_all_accounts(self) -> List[BankAccount]:
        """
        Получить все счета.
        Returns:
            Список всех счетов в коллекции
        """
        return self._accounts.copy()

    def get_accounts_count(self) -> int:
        """
        Получить количество счетов.
        Returns:
            Количество счетов в коллекции
        """
        return len(self._accounts)

    def _find_by_number(self, account_number: str) -> Optional[BankAccount]:
        """Вспомогательный метод: найти счет по номеру."""
        for acc in self._accounts:
            if acc.account_number == account_number:
                return acc
        return None

    def find_account_by_number(self, account_number: str) -> BankAccount:
        """
        Найти счет по номеру.
        Args:
            account_number: Номер счета
        Returns:
            Найденный счет
        Raises:
            AccountNotFoundError: Если счет не найден
        """
        account = self._find_by_number(account_number)
        if not account:
            raise AccountNotFoundError(f"Счет {account_number} не найден")
        return account

    def find_accounts_by_owner(self, owner_name: str) -> List[BankAccount]:
        """
        Найти все счета по имени владельца (частичный поиск).

        Args:
            owner_name: Часть имени владельца

        Returns:
            Список найденных счетов
        """
        return [
            acc for acc in self._accounts
            if owner_name.lower() in acc.owner_name.lower()
        ]

    def find_accounts_by_status(self, status: AccountStatus) -> List[BankAccount]:
        """
        Найти все счета по статусу.
        Args:
            status: Статус счета
        Returns:
            Список счетов с заданным статусом
        """
        return [acc for acc in self._accounts if acc.status == status]

    def filter_accounts(self, predicate: Callable[[BankAccount], bool]) -> List[BankAccount]:
        """
        Фильтровать счета по условию.
        Args:
            predicate: Функция-предикат для фильтрации
        Returns:
            Список счетов, удовлетворяющих условию
        """
        return [acc for acc in self._accounts if predicate(acc)]

    def sort_accounts(self, sort_by: str, reverse: bool = False) -> List[BankAccount]:
        """
        Отсортировать счета по выбранной стратегии.
        Args:
            sort_by: Ключ сортировки (owner_name, balance, created_date)
            reverse: Сортировать по убыванию, если True
        Returns:
            Отсортированный список счетов
        Raises:
            OperationError: Если указан неизвестный способ сортировки
        """
        sorters: dict[str, Callable[[BankAccount], object]] = {
            "owner_name": by_owner_name,
            "balance": by_balance,
            "created_date": lambda acc: acc.created_date,
        }

        if sort_by not in sorters:
            raise OperationError(f"Неверный способ сортировки: {sort_by}")

        return sorted(self._accounts, key=sorters[sort_by], reverse=reverse)

    def remove_account(self, account_number: str) -> BankAccount:
        """
        Удалить счет из коллекции.
        Args:
            account_number: Номер счета для удаления
        Returns:
            Удаленный счет
        Raises:
            AccountNotFoundError: Если счет не найден
            OperationError: Если счет не может быть удален
        """
        account = self.find_account_by_number(account_number)

        if account.balance != 0:
            raise OperationError(
                f"Невозможно удалить счет с ненулевым балансом ({account.balance:.2f})"
            )

        self._accounts.remove(account)
        return account

    def deposit(self, account_number: str, amount: float,
                description: str = "Пополнение") -> None:
        """
        Пополнить счет.
        Args:
            account_number: Номер счета
            amount: Сумма пополнения
            description: Описание операции
        Raises:
            AccountNotFoundError: Если счет не найден
            OperationError: При ошибке во время операции
        """
        account = self.find_account_by_number(account_number)
        try:
            account.deposit(amount, description)
        except ValueError as e:
            raise OperationError(str(e))

    def withdraw(self, account_number: str, amount: float,
                 description: str = "Снятие") -> None:
        """
        Снять деньги со счета.
        Args:
            account_number: Номер счета
            amount: Сумма снятия
            description: Описание операции
        Raises:
            AccountNotFoundError: Если счет не найден
            OperationError: При ошибке во время операции
        """
        account = self.find_account_by_number(account_number)
        try:
            account.withdraw(amount, description)
        except ValueError as e:
            raise OperationError(str(e))

    def transfer(self, from_account_number: str, to_account_number: str,
                 amount: float, description: str = "Перевод") -> None:
        """
        Перевести деньги между счетами.
        Args:
            from_account_number: Номер счета-отправителя
            to_account_number: Номер счета-получателя
            amount: Сумма перевода
            description: Описание операции
        Raises:
            AccountNotFoundError: Если счет не найден
            OperationError: При ошибке во время операции
        """
        from_account = self.find_account_by_number(from_account_number)
        to_account = self.find_account_by_number(to_account_number)
        try:
            from_account.transfer(to_account, amount, description)
        except ValueError as e:
            raise OperationError(str(e))

    def apply_savings_interest(self, account_number: str) -> float:
        """
        Начислить проценты на сберегательный счет.
        Args:
            account_number: Номер счета
        Returns:
            Размер начисленных процентов
        Raises:
            AccountNotFoundError: Если счет не найден
            OperationError: Если счет не сберегательный
        """
        account = self.find_account_by_number(account_number)
        if not isinstance(account, SavingsAccount):
            raise OperationError("Операция доступна только для сберегательных счетов")

        return account.apply_interest()

    def block_account(self, account_number: str) -> None:
        """
        Заблокировать счет.
        Args:
            account_number: Номер счета
        Raises:
            AccountNotFoundError: Если счет не найден
        """
        account = self.find_account_by_number(account_number)
        account.block()

    def activate_account(self, account_number: str) -> None:
        """
        Активировать счет.
        Args:
            account_number: Номер счета
        Raises:
            AccountNotFoundError: Если счет не найден
        """
        account = self.find_account_by_number(account_number)
        account.activate()

    def get_account_info(self, account_number: str) -> dict:
        """
        Получить полную информацию о счете.
        Args:
            account_number: Номер счета
        Returns:
            Словарь с информацией о счете
        Raises:
            AccountNotFoundError: Если счет не найден
        """
        account = self.find_account_by_number(account_number)
        return account.get_account_info()

    def set_loaded_accounts(self, accounts: List[BankAccount]) -> None:
        """
        Установить загруженные счета (для восстановления из хранилища).
        Args:
            accounts: Список счетов для загрузки
        """
        self._accounts = accounts.copy()

