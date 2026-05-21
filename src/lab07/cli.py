"""
CLI интерфейс приложения управления банковскими счетами.
"""

import sys
from pathlib import Path
from typing import Optional, Callable

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
from app import BankApp
from exceptions import (
    BankAppException, AccountNotFoundError, OperationError
)


class BankCLI:
    """Интерфейс командной строки для работы с банковским приложением."""

    def __init__(self, app: BankApp) -> None:
        """
        Инициализация CLI.
        Args:
            app: Экземпляр BankApp для работы с данными
        """
        self._app = app
        self._running = True

    def run(self) -> None:
        """Запустить основной цикл приложения."""
        self._print_welcome()
        first_iteration = True

        while self._running:
            try:
                # Показываем меню только в первый раз и если попросили повторить
                if first_iteration:
                    self._show_main_menu()
                    first_iteration = False

                choice = self._get_input("➤ Выбор: ").strip()
                if not choice:
                    continue

                self._handle_main_menu(choice)

                # Показываем меню перед следующей итерацией
                if self._running:
                    self._show_main_menu()
            except KeyboardInterrupt:
                print("\n\n⚠️  Приложение прервано пользователем")
                self._running = False
            except BankAppException as e:
                print(f"\n❌ Ошибка: {e}")
            except Exception as e:
                print(f"\n❌ Непредвиденная ошибка: {e}")

    def _print_welcome(self) -> None:
        """Вывести приветственное сообщение."""
        print("\n" + "="*70)
        print("🏦  СИСТЕМА УПРАВЛЕНИЯ БАНКОВСКИМИ СЧЕТАМИ (ЛР-7)")
        print("="*70 + "\n")

    def _show_main_menu(self) -> None:
        """Вывести главное меню."""
        print("\n" + "-"*70)
        print("ГЛАВНОЕ МЕНЮ")
        print("-"*70)
        print("1. Показать все счета")
        print("2. Добавить новый счет")
        print("3. Найти счет")
        print("4. Операции со счетом (пополнение/снятие/перевод)")
        print("5. Специальные операции (проценты, статус)")
        print("6. Удалить счет")
        print("7. Сортировка и фильтрация")
        print("0. Выход")
        print("-"*70)

    def _handle_main_menu(self, choice: str) -> None:
        """
        Обработать выбор из главного меню.
        Args:
            choice: Выбор пользователя
        """
        if choice == "1":
            self._show_all_accounts()
        elif choice == "2":
            self._add_account()
        elif choice == "3":
            self._find_account_menu()
        elif choice == "4":
            self._operations_menu()
        elif choice == "5":
            self._special_operations_menu()
        elif choice == "6":
            self._delete_account()
        elif choice == "7":
            self._analysis_menu()
        elif choice == "0":
            self._running = False
            print("\n👋 Спасибо за использование приложения!\n")
        else:
            print("❌ Неверный выбор. Попробуйте снова.")

    def _show_all_accounts(self) -> None:
        """Показать все счета в таблице."""
        accounts = self._app.get_all_accounts()

        if not accounts:
            print("\n Счетов не найдено")
            return

        print(f"\n СЧЕТА ({len(accounts)} шт.)")
        print("="*70)

        for i, acc in enumerate(accounts, 1):
            acc_type = "Кредитный" if isinstance(acc, CreditAccount) else \
                       "Сберегательный" if isinstance(acc, SavingsAccount) else "Базовый"

            status_emoji = "🟢" if acc.status == AccountStatus.ACTIVE else \
                          "🔴" if acc.status == AccountStatus.BLOCKED else "🟠"

            print(f"\n{i}. {status_emoji} {acc.account_number} | {acc_type}")
            print(f"   Владелец: {acc.owner_name}")
            print(f"   Баланс: {acc.balance:>12.2f} {acc.currency}")
            print(f"   Статус: {acc.status.value}")

            if isinstance(acc, SavingsAccount):
                print(f"   Ставка: {acc.interest_rate}%")
            elif isinstance(acc, CreditAccount):
                print(f"   Кредитный лимит: {acc.credit_limit:>8.2f} {acc.currency}")
                print(f"   Использовано: {acc.used_credit:>12.2f} {acc.currency}")

        print("\n" + "="*70)

    def _print_accounts_collection(self, accounts, title: str) -> None:
        """Вывести список счетов в структурированном виде."""
        if not accounts:
            print(f"\n📭 {title}: счетов не найдено")
            return

        print(f"\n📋 {title} ({len(accounts)} шт.)")
        print("=" * 70)

        for i, acc in enumerate(accounts, 1):
            acc_type = "Кредитный" if isinstance(acc, CreditAccount) else \
                       "Сберегательный" if isinstance(acc, SavingsAccount) else "Базовый"
            status_emoji = "🟢" if acc.status == AccountStatus.ACTIVE else \
                          "🔴" if acc.status == AccountStatus.BLOCKED else "🟠"

            print(f"\n{i}. {status_emoji} {acc.account_number} | {acc_type}")
            print(f"   Владелец: {acc.owner_name}")
            print(f"   Баланс: {acc.balance:>12.2f} {acc.currency}")
            print(f"   Статус: {acc.status.value}")

            if isinstance(acc, SavingsAccount):
                print(f"   Ставка: {acc.interest_rate}%")
            elif isinstance(acc, CreditAccount):
                print(f"   Кредитный лимит: {acc.credit_limit:>8.2f} {acc.currency}")
                print(f"   Использовано: {acc.used_credit:>12.2f} {acc.currency}")

        print("\n" + "=" * 70)

    def _add_account(self) -> None:
        """Добавить новый счет."""
        print("\n ДОБАВЛЕНИЕ НОВОГО СЧЕТА")
        print("-"*70)
        print("Тип счета:")
        print("1. Базовый")
        print("2. Сберегательный")
        print("3. Кредитный")

        account_type = self._get_input("Выберите тип (1-3): ").strip()

        owner_name = self._get_input("ФИО владельца: ").strip()
        if len(owner_name) < 3:
            raise OperationError("ФИО должно содержать минимум 3 символа")

        currency = self._get_input("Валюта (RUB/USD/EUR/GBP/CNY): ").strip().upper()
        if currency not in ["RUB", "USD", "EUR", "GBP", "CNY"]:
            raise OperationError("Неподдерживаемая валюта")

        initial_balance = self._get_float("Начальный баланс (0-1000000000): ")
        if initial_balance < 0:
            raise OperationError("Баланс не может быть отрицательным")

        try:
            if account_type == "1":
                account = BankAccount(owner_name, currency, initial_balance)
            elif account_type == "2":
                interest_rate = self._get_float("Процентная ставка (0-20): ")
                if not (0 <= interest_rate <= 20):
                    raise OperationError("Ставка должна быть от 0 до 20%")
                account = SavingsAccount(owner_name, currency, initial_balance, interest_rate)
            elif account_type == "3":
                credit_limit = self._get_float("Кредитный лимит (1-1000000): ")
                if credit_limit <= 0:
                    raise OperationError("Лимит должен быть положительным")
                interest = self._get_float("Процент по долгу (0-30): ")
                if not (0 <= interest <= 30):
                    raise OperationError("Процент должен быть от 0 до 30%")
                account = CreditAccount(owner_name, currency, credit_limit, interest)
            else:
                raise OperationError("Неверный тип счета")

            self._app.add_account(account)
            print(f"\n✅ Счет создан: {account.account_number}")
        except ValueError as e:
            raise OperationError(str(e))

    def _find_account_menu(self) -> None:
        """Меню поиска счетов."""
        print("\n🔍 ПОИСК СЧЕТА")
        print("-"*70)
        print("1. По номеру счета")
        print("2. По имени владельца")
        print("3. По статусу")

        choice = self._get_input("Выберите способ поиска: ")

        if choice == "1":
            account_number = self._get_input("Номер счета: ").strip()
            account = self._app.find_account_by_number(account_number)
            self._print_account_details(account)
        elif choice == "2":
            owner_name = self._get_input("Часть имени владельца: ").strip()
            accounts = self._app.find_accounts_by_owner(owner_name)
            if accounts:
                for i, acc in enumerate(accounts, 1):
                    print(f"\n{i}. {acc.account_number} - {acc.owner_name} ({acc.status.value})")
                    print(f"   Баланс: {acc.balance:.2f} {acc.currency}")
            else:
                print("❌ Счетов не найдено")
        elif choice == "3":
            print("Статусы: 1=активен, 2=заблокирован, 3=заморожен")
            status_choice = self._get_input("Выберите статус: ")

            status_map = {
                "1": AccountStatus.ACTIVE,
                "2": AccountStatus.BLOCKED,
                "3": AccountStatus.FROZEN,
            }

            if status_choice not in status_map:
                raise OperationError("Неверный статус")

            accounts = self._app.find_accounts_by_status(status_map[status_choice])
            if accounts:
                print(f"\n📋 Найдено счетов со статусом '{status_map[status_choice].value}': {len(accounts)}")
                for i, acc in enumerate(accounts, 1):
                    print(f"{i}. {acc.account_number} - {acc.owner_name} ({acc.balance:.2f} {acc.currency})")
            else:
                print("❌ Счетов не найдено")
        else:
            raise OperationError("Неверный выбор")

    def _print_account_details(self, account: BankAccount) -> None:
        """Вывести полную информацию о счете."""
        print("\n" + "="*70)
        print(" ИНФОРМАЦИЯ О СЧЕТЕ")
        print("="*70)
        print(account)
        print("="*70)

    def _operations_menu(self) -> None:
        """Меню операций со счетом."""
        account_number = self._get_input("Номер счета: ").strip()
        self._app.find_account_by_number(account_number)  # Проверка существования

        print("\nОПЕРАЦИИ")
        print("1.  Пополнение счета")
        print("2.  Снятие со счета")
        print("3.  Перевод на другой счет")

        choice = self._get_input("Выберите операцию: ")

        if choice == "1":
            amount = self._get_float("Сумма пополнения: ")
            description = self._get_input("Описание (Enter для пропуска): ").strip()
            self._app.deposit(account_number, amount,
                            description or "Пополнение счета")
            print("✅ Пополнение выполнено")
        elif choice == "2":
            amount = self._get_float("Сумма снятия: ")
            description = self._get_input("Описание (Enter для пропуска): ").strip()
            self._app.withdraw(account_number, amount,
                             description or "Снятие со счета")
            print("✅ Снятие выполнено")
        elif choice == "3":
            to_account = self._get_input("Номер счета-получателя: ").strip()
            amount = self._get_float("Сумма перевода: ")
            self._app.transfer(account_number, to_account, amount)
            print("✅ Перевод выполнен")
        else:
            raise OperationError("Неверный выбор")

    def _special_operations_menu(self) -> None:
        """Меню специальных операций."""
        print("\nСПЕЦИАЛЬНЫЕ ОПЕРАЦИИ")
        print("1. Начислить проценты (сберегательн. счет)")
        print("2. 🔴 Заблокировать счет")
        print("3. 🟢 Активировать счет")
        print("4.  История транзакций")

        choice = self._get_input("Выберите операцию: ")
        account_number = self._get_input("Номер счета: ").strip()

        if choice == "1":
            interest = self._app.apply_savings_interest(account_number)
            print(f"✅ Проценты начислены: {interest:.2f}")
        elif choice == "2":
            self._app.block_account(account_number)
            print("✅ Счет заблокирован")
        elif choice == "3":
            self._app.activate_account(account_number)
            print("✅ Счет активирован")
        elif choice == "4":
            account = self._app.find_account_by_number(account_number)
            history = account.get_transaction_history(limit=10)
            if history:
                print(f"\n История транзакций (последние {len(history)}):")
                for i, trans in enumerate(history, 1):
                    print(f"{i}. {trans['type']:15} {trans['amount']:>12.2f} - {trans['description']}")
            else:
                print(" История пуста")
        else:
            raise OperationError("Неверный выбор")

    def _delete_account(self) -> None:
        """Удалить счет."""
        account_number = self._get_input("Номер счета для удаления: ").strip()
        account = self._app.find_account_by_number(account_number)

        print(f"\n⚠️  Удаление счета {account_number}")
        print(f"   Владелец: {account.owner_name}")
        print(f"   Баланс: {account.balance:.2f}")

        if account.balance != 0:
            print("❌ Невозможно удалить счет с ненулевым балансом!")
            return

        confirm = self._get_input("\nВы уверены? (y/n): ").lower()
        if confirm == "y":
            self._app.remove_account(account_number)
            print("✅ Счет удален")
        else:
            print("❌ Удаление отменено")

    def _analysis_menu(self) -> None:
        """Меню сортировки и фильтрации."""
        print("\n СОРТИРОВКА И ФИЛЬТРАЦИЯ")
        print("-" * 70)
        print("1. Сортировка счетов")
        print("2. Фильтрация счетов")

        choice = self._get_input("Выберите раздел: ").strip()

        if choice == "1":
            self._sort_accounts_menu()
        elif choice == "2":
            self._filter_accounts_menu()
        else:
            raise OperationError("Неверный выбор")

    def _sort_accounts_menu(self) -> None:
        """Меню сортировки счетов."""
        print("\n СОРТИРОВКА СЧЕТОВ")
        print("-" * 70)
        print("1. По имени владельца")
        print("2. По балансу")
        print("3. По дате открытия")

        choice = self._get_input("Выберите стратегию: ").strip()
        order = self._get_input("Сортировать по убыванию? (y/n): ").strip().lower()
        reverse = order == "y"

        if choice == "1":
            accounts = self._app.sort_accounts("owner_name", reverse=reverse)
            title = "Счета, отсортированные по имени владельца"
        elif choice == "2":
            accounts = self._app.sort_accounts("balance", reverse=reverse)
            title = "Счета, отсортированные по балансу"
        elif choice == "3":
            accounts = self._app.sort_accounts("created_date", reverse=reverse)
            title = "Счета, отсортированные по дате открытия"
        else:
            raise OperationError("Неверный выбор")

        self._print_accounts_collection(accounts, title)

    def _filter_accounts_menu(self) -> None:
        """Меню фильтрации счетов."""
        print("\n ФИЛЬТРАЦИЯ И АНАЛИТИКА")
        print("-"*70)
        print("1. По минимальному балансу")
        print("2. По валюте")
        print("3. По диапазону баланса")
        print("4. Счета со сберегательным процентом > X%")

        choice = self._get_input("Выберите фильтр: ")

        if choice == "1":
            min_balance = self._get_float("Минимальный баланс: ")
            accounts = self._app.filter_accounts(lambda acc: acc.balance >= min_balance)
            self._print_filtered_accounts(accounts,
                f"Счета с балансом >= {min_balance:.2f}")

        elif choice == "2":
            currency = self._get_input("Валюта (RUB/USD/EUR): ").strip().upper()
            accounts = self._app.filter_accounts(lambda acc: acc.currency == currency)
            self._print_filtered_accounts(accounts, f"Счета в {currency}")

        elif choice == "3":
            min_bal = self._get_float("Минимальный баланс: ")
            max_bal = self._get_float("Максимальный баланс: ")
            accounts = self._app.filter_accounts(
                lambda acc: min_bal <= acc.balance <= max_bal
            )
            self._print_filtered_accounts(accounts,
                f"Счета с балансом от {min_bal:.2f} до {max_bal:.2f}")

        elif choice == "4":
            min_rate = self._get_float("Минимальная ставка (%): ")
            accounts = self._app.filter_accounts(
                lambda acc: isinstance(acc, SavingsAccount) and acc.interest_rate >= min_rate
            )
            self._print_filtered_accounts(accounts,
                f"Сберегательные счета со ставкой >= {min_rate}%")

        else:
            raise OperationError("Неверный выбор")

    def _print_filtered_accounts(self, accounts, title: str) -> None:
        """Вывести отфильтрованные счета."""
        if not accounts:
            print(f"\n❌ {title}: счетов не найдено")
            return

        print(f"\n✅ {title}: {len(accounts)} счет(а)")
        print("-"*70)

        total_balance: dict = {}
        for acc in accounts:
            if acc.currency not in total_balance:
                total_balance[acc.currency] = 0.0
            total_balance[acc.currency] += acc.balance

            print(f"📌 {acc.account_number} | {acc.owner_name}")
            print(f"   Баланс: {acc.balance:>12.2f} {acc.currency} | Статус: {acc.status.value}")

        print("-"*70)
        print("ИТОГО:")
        for currency, total in total_balance.items():
            print(f"  {currency}: {total:>12.2f}")

    def _get_input(self, prompt: str = "") -> str:
        """
        Получить строку от пользователя.
        Args:
            prompt: Приглашение для ввода
        Returns:
            Введённая строка
        """
        print(prompt, end="", flush=True)
        return input()

    def _get_float(self, prompt: str = "") -> float:
        """
        Получить число от пользователя.
        Args:
            prompt: Приглашение для ввода
        Returns:
            Введённое число
        Raises:
            OperationError: Если ввод не является числом
        """
        while True:
            try:
                print(prompt, end="", flush=True)
                return float(input())
            except ValueError:
                print("❌ Ошибка: введите корректное число")

