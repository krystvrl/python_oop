"""
Модуль с дочерними классами банковских счетов.
SavingsAccount и CreditAccount - наследники BankAccount.
"""

from datetime import date
from typing import Optional

from base import BankAccount, AccountStatus


class SavingsAccount(BankAccount):
    """
    Сберегательный счет.
    Особенности: начисление процентов на остаток.
    """
    
    DEFAULT_INTEREST_RATE = 5.0  # 5% годовых
    MIN_BALANCE_MAINTAINED = 1000.0

    def __init__(self, owner_name: str, currency: str = "RUB",
                 initial_balance: float = 0.0, interest_rate: Optional[float] = None):
        """
        Конструктор сберегательного счета.
        Доп. атрибуты: interest_rate, last_interest_date
        """
        super().__init__(owner_name, currency, initial_balance)
        
        # Новые атрибуты
        self.interest_rate = (SavingsAccount.DEFAULT_INTEREST_RATE
                              if interest_rate is None else interest_rate)
        self.__min_balance_maintained = SavingsAccount.MIN_BALANCE_MAINTAINED
        self.__last_interest_date = date.today()
    
    @property
    def interest_rate(self) -> float:
        """Процентная ставка."""
        return self.__interest_rate
    
    @interest_rate.setter
    def interest_rate(self, value: float):
        if value < 0:
            raise ValueError("Процентная ставка не может быть отрицательной")
        if value > 20:
            raise ValueError("Процентная ставка не может превышать 20%")
        self.__interest_rate = value

    @property
    def min_balance_maintained(self) -> float:
        """Минимальный остаток на счете."""
        return self.__min_balance_maintained

    @property
    def last_interest_date(self) -> date:
        """Дата последнего начисления процентов."""
        return self.__last_interest_date

    def apply_interest(self) -> float:
        """Начисление процентов на остаток по счету."""
        if self.status in (AccountStatus.BLOCKED, AccountStatus.CLOSED):
            raise ValueError("Нельзя начислить проценты на неактивный счет")

        interest = self.balance * (self.__interest_rate / 100)
        
        if interest > 0:
            self.deposit(interest, f"Начисление процентов {self.__interest_rate}%")
            self.__last_interest_date = date.today()
        
        return interest
    
    def check_min_balance(self) -> bool:
        """Проверка соблюдения минимального остатка."""
        return self.balance >= self.__min_balance_maintained

    def calculate_annual_interest(self) -> float:
        """Расчет годового дохода от процентов."""
        return self.balance * (self.__interest_rate / 100)

    def calculate_annual_income(self) -> float:
        """Совместимый алиас для старого названия метода."""
        return self.calculate_annual_interest()

    def __str__(self) -> str:
        base_str = super().__str__()
        return (base_str + f"\n   💰 Тип: Сберегательный счет\n"
                f"   📈 Ставка: {self.__interest_rate}%\n"
                f"   📉 Мин. остаток: {self.__min_balance_maintained:,.2f} {self.currency}\n"
                f"   📅 Последние проценты: {self.__last_interest_date.strftime('%d.%m.%Y')}")
    
    def __repr__(self) -> str:
        return (f"SavingsAccount(owner_name='{self.owner_name}', "
                f"currency='{self.currency}', "
                f"balance={self.balance:.2f}, "
                f"interest_rate={self.__interest_rate}, "
                f"min_balance_maintained={self.__min_balance_maintained})")


class CreditAccount(BankAccount):
    """
    Кредитный счет.
    Особенности: кредитный лимит, баланс может быть отрицательным.
    """
    
    DEFAULT_CREDIT_LIMIT = 50000.0
    DEFAULT_INTEREST_ON_DEBT = 15.0

    def __init__(self, owner_name: str, currency: str = "RUB",
                 credit_limit: Optional[float] = None,
                 interest_on_debt: Optional[float] = None):
        """
        Конструктор кредитного счета.
        Доп. атрибуты: credit_limit, credit_used
        """
        super().__init__(owner_name, currency, initial_balance=0.0)
        
        # Новые атрибуты
        self.credit_limit = (CreditAccount.DEFAULT_CREDIT_LIMIT
                             if credit_limit is None else credit_limit)
        self.__credit_used = 0.0  # Сколько кредитных средств использовано
        self.interest_on_debt = (CreditAccount.DEFAULT_INTEREST_ON_DEBT
                                 if interest_on_debt is None else interest_on_debt)

    @property
    def credit_limit(self) -> float:
        """Кредитный лимит."""
        return self.__credit_limit

    @credit_limit.setter
    def credit_limit(self, value: float):
        if value <= 0:
            raise ValueError("Кредитный лимит должен быть положительным")
        if hasattr(self, "_CreditAccount__credit_used") and value < self.__credit_used:
            raise ValueError("Кредитный лимит не может быть меньше использованного кредита")
        self.__credit_limit = value

    @property
    def used_credit(self) -> float:
        """Использованный кредит."""
        return self.__credit_used

    @property
    def credit_used(self) -> float:
        """Совместимый алиас для старого названия свойства."""
        return self.__credit_used

    @property
    def interest_on_debt(self) -> float:
        """Процент по задолженности."""
        return self.__interest_on_debt

    @interest_on_debt.setter
    def interest_on_debt(self, value: float):
        if value < 0:
            raise ValueError("Процент по задолженности не может быть отрицательным")
        self.__interest_on_debt = value

    @property
    def available_credit(self) -> float:
        """Доступный кредит."""
        return self.__credit_limit - self.__credit_used
    
    def credit_withdraw(self, amount: float, description: str = "Снятие со счета") -> dict:
        """
        Снятие средств. Если не хватает денег, используется кредит.
        """
        if amount <= 0:
            raise ValueError(f"Сумма снятия должна быть положительной: {amount}")
        
        if self.status == AccountStatus.BLOCKED:
            raise ValueError("Счет заблокирован. Операция невозможна")
        
        if self.status == AccountStatus.CLOSED:
            raise ValueError("Счет закрыт. Операция невозможна")
        
        if self.status == AccountStatus.FROZEN:
            raise ValueError("Счет заморожен. Снятие средств невозможно")

        old_balance = self.balance
        old_used_credit = self.__credit_used
        projected_balance = old_balance - amount
        projected_used_credit = max(0.0, -projected_balance)

        if projected_used_credit > self.__credit_limit:
            raise ValueError(f"Превышение кредитного лимита. "
                             f"Доступно: {self.available_credit:.2f} {self.currency}")

        self._BankAccount__balance = projected_balance
        self.__credit_used = projected_used_credit

        credit_delta = self.__credit_used - old_used_credit
        if credit_delta > 0:
            self._add_transaction("CREDIT_USED", credit_delta,
                                  f"Использование кредита: {description}")

        return self._add_transaction("WITHDRAWAL", amount, description)

    def withdraw(self, amount: float, description: str = "Снятие со счета") -> dict:
        """Совместимый алиас для снятия с учетом кредитного лимита."""
        return self.credit_withdraw(amount, description)

    def deposit(self, amount: float, description: str = "Пополнение счета") -> dict:
        """
        Пополнение счета. Сначала погашается кредит, остаток идет на баланс.
        """
        if amount <= 0:
            raise ValueError(f"Сумма пополнения должна быть положительной: {amount}")
        
        if self.status == AccountStatus.BLOCKED:
            raise ValueError("Счет заблокирован. Операция невозможна")
        
        if self.status == AccountStatus.CLOSED:
            raise ValueError("Счет закрыт. Операция невозможна")

        old_used_credit = self.__credit_used
        projected_balance = self.balance + amount
        projected_used_credit = max(0.0, -projected_balance)

        self._BankAccount__balance = projected_balance
        self.__credit_used = projected_used_credit

        repayment = old_used_credit - projected_used_credit
        if repayment > 0:
            self._add_transaction("CREDIT_REPAYMENT", repayment,
                                  f"Погашение кредита: {description}")

        return self._add_transaction("DEPOSIT", amount, description)
    
    def calculate_debt_interest(self) -> float:
        """Расчет процентов по кредитной задолженности."""
        return self.__credit_used * (self.__interest_on_debt / 100)

    def calculate_annual_interest(self) -> float:
        """Для кредитного счета доход отрицательный (расходы)."""
        value = -self.calculate_debt_interest()
        return 0.0 if abs(value) < 1e-12 else value

    def calculate_annual_income(self) -> float:
        """Совместимый алиас для старого названия метода."""
        return self.calculate_annual_interest()

    def __str__(self) -> str:
        base_str = super().__str__()
        balance_str = f"{self.balance:,.2f}" if self.balance >= 0 else f"({abs(self.balance):,.2f})"
        return (base_str + f"\n   💳 Тип: Кредитный счет\n"
                f"   💳 Кредитный лимит: {self.__credit_limit:>12,.2f} {self.currency}\n"
                f"   📊 Использовано кредита: {self.__credit_used:>9,.2f} {self.currency}\n"
                f"   📈 Процент по долгу: {self.__interest_on_debt:>10,.2f}%\n"
                f"   🟢 Доступно: {self.available_credit:>12,.2f} {self.currency}\n"
                f"   📍 Реальный баланс: {balance_str} {self.currency}")
    
    def __repr__(self) -> str:
        return (f"CreditAccount(owner_name='{self.owner_name}', "
                f"currency='{self.currency}', "
                f"balance={self.balance:.2f}, "
                f"credit_limit={self.__credit_limit}, "
                f"used_credit={self.__credit_used}, "
                f"interest_on_debt={self.__interest_on_debt})")