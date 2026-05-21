"""
Модуль для сохранения и загрузки банковских счетов в/из JSON.
"""

import json
import sys
from pathlib import Path
from datetime import datetime, date
from typing import Optional, List, Dict, Any

# Добавляем путь к lab03 для импорта классов
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
from exceptions import StorageError


class BankAccountEncoder(json.JSONEncoder):
    """Кодировщик для сохранения объектов BankAccount в JSON."""

    def default(self, obj: Any) -> Any:
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        if isinstance(obj, AccountStatus):
            return obj.value
        return super().default(obj)


def _serialize_account(account: BankAccount) -> Dict[str, Any]:
    """Сериализация одного счета в словарь."""
    info = account.get_account_info()
    account_type = "credit" if isinstance(account, CreditAccount) else \
                   "savings" if isinstance(account, SavingsAccount) else "basic"

    data: Dict[str, Any] = {
        "type": account_type,
        **info,
        "transactions": account.get_transaction_history(),
    }

    if isinstance(account, SavingsAccount):
        data["interest_rate"] = account.interest_rate
    elif isinstance(account, CreditAccount):
        data["credit_limit"] = account.credit_limit
        data["used_credit"] = account.used_credit
        data["interest_on_debt"] = account.interest_on_debt

    return data


def _deserialize_account(data: Dict[str, Any]) -> BankAccount:
    """Десериализация словаря в объект BankAccount."""
    account_type = data.pop("type", "basic")
    account_number = data.pop("account_number", None)
    owner_name = data.pop("owner_name")
    currency = data.pop("currency")
    balance = data.pop("balance")
    created_date = data.pop("created_date", None)

    if account_type == "savings":
        interest_rate = data.pop("interest_rate", 5.0)
        account = SavingsAccount(owner_name, currency, balance, interest_rate)
    elif account_type == "credit":
        credit_limit = data.pop("credit_limit", 50000.0)
        interest_on_debt = data.pop("interest_on_debt", 15.0)
        account = CreditAccount(owner_name, currency, credit_limit, interest_on_debt)
    else:
        account = BankAccount(owner_name, currency, balance)

    # Восстанавливаем баланс и специфичные поля после создания объекта.
    if isinstance(account, CreditAccount):
        account._BankAccount__balance = balance
        account._CreditAccount__credit_used = float(
            data.pop("used_credit", max(0.0, -balance))
        )

    if account_type in {"basic", "savings"}:
        account._BankAccount__balance = balance

    # Восстанавливаем статус счета
    status_str = data.pop("status", "активен")
    for status in AccountStatus:
        if status.value == status_str:
            if status != AccountStatus.ACTIVE:
                account._BankAccount__status = status
            break

    if created_date:
        try:
            account._BankAccount__created_date = datetime.strptime(
                created_date, "%d.%m.%Y"
            ).date()
        except ValueError:
            pass

    if account_number:
        account._BankAccount__account_number = account_number
        try:
            counter_value = int(str(account_number).replace("40817810", ""))
            BankAccount._account_counter = max(BankAccount._account_counter, counter_value + 1)
        except ValueError:
            pass

    return account


def save_accounts(accounts: List[BankAccount], filepath: str) -> None:
    """
    Сохранить список счетов в JSON-файл.
    Args:
        accounts: Список банковских счетов для сохранения
        filepath: Путь к файлу для сохранения
    Raises:
        StorageError: При ошибке записи файла
    """
    try:
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)

        data = {
            "saved_at": datetime.now().isoformat(),
            "accounts": [_serialize_account(acc) for acc in accounts]
        }

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, cls=BankAccountEncoder, indent=2, ensure_ascii=False)
    except Exception as e:
        raise StorageError(f"Ошибка при сохранении данных: {e}")


def load_accounts(filepath: str) -> List[BankAccount]:
    """
    Загрузить список счетов из JSON-файла.
    Args:
        filepath: Путь к файлу для загрузки
    Returns:
        Список загруженных банковских счетов
    Raises:
        StorageError: При ошибке чтения или парсинга файла
    """
    try:
        path = Path(filepath)

        if not path.exists():
            return []

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        accounts: List[BankAccount] = []
        for account_data in data.get("accounts", []):
            account = _deserialize_account(account_data)
            accounts.append(account)

        return accounts
    except json.JSONDecodeError as e:
        raise StorageError(f"Ошибка при чтении JSON: {e}")
    except Exception as e:
        raise StorageError(f"Ошибка при загрузке данных: {e}")

