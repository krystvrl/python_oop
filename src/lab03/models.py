"""
Модуль с дочерними классами банковских счетов.
SavingsAccount и CreditAccount - наследники BankAccount.
"""

from datetime import date
from base import BankAccount, AccountStatus


class SavingsAccount(BankAccount):
    """
    Сберегательный счет.
    Особенности: начисление процентов на остаток.
    """
    
    DEFAULT_INTEREST_RATE = 5.0  # 5% годовых
    
    def __init__(self, owner_name: str, currency: str = "RUB",
                 initial_balance: float = 0.0, interest_rate: float = None):
        """
        Конструктор сберегательного счета.
        Доп. атрибуты: interest_rate, last_interest_date
        """
        super().__init__(owner_name, currency, initial_balance)
        
        # Новые атрибуты
        self.__interest_rate = interest_rate if interest_rate else SavingsAccount.DEFAULT_INTEREST_RATE
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
    
    # Новый метод 1
    def apply_interest(self) -> float:
        """Начисление процентов на остаток по счету."""
        if self.status == AccountStatus.CLOSED:
            raise ValueError("Нельзя начислить проценты на закрытый счет")
        
        interest = self.balance * (self.__interest_rate / 100)
        
        if interest > 0:
            self.deposit(interest, f"Начисление процентов {self.__interest_rate}%")
            self.__last_interest_date = date.today()
        
        return interest
    
    # Новый метод 2
    def days_since_last_interest(self) -> int:
        """Количество дней с последнего начисления процентов."""
        delta = date.today() - self.__last_interest_date
        return delta.days
    
    # Переопределенный метод
    def calculate_annual_income(self) -> float:
        """Расчет годового дохода от процентов."""
        return self.balance * (self.__interest_rate / 100)
    
    def __str__(self) -> str:
        base_str = super().__str__()
        return (base_str + f"\n   💰 Тип: Сберегательный счет\n"
                f"   📈 Ставка: {self.__interest_rate}%\n"
                f"   📅 Последние проценты: {self.__last_interest_date.strftime('%d.%m.%Y')}")
    
    def __repr__(self) -> str:
        return (f"SavingsAccount(owner_name='{self.owner_name}', "
                f"currency='{self.currency}', "
                f"balance={self.balance:.2f}, "
                f"interest_rate={self.__interest_rate})")


class CreditAccount(BankAccount):
    """
    Кредитный счет.
    Особенности: кредитный лимит, баланс может быть отрицательным.
    """
    
    DEFAULT_CREDIT_LIMIT = 50000.0
    
    def __init__(self, owner_name: str, currency: str = "RUB",
                 credit_limit: float = None):
        """
        Конструктор кредитного счета.
        Доп. атрибуты: credit_limit, credit_used
        """
        super().__init__(owner_name, currency, initial_balance=0.0)
        
        # Новые атрибуты
        self.__credit_limit = credit_limit if credit_limit else CreditAccount.DEFAULT_CREDIT_LIMIT
        self.__credit_used = 0.0  # Сколько кредитных средств использовано
    
    @property
    def credit_limit(self) -> float:
        """Кредитный лимит."""
        return self.__credit_limit
    
    @property
    def credit_used(self) -> float:
        """Использованный кредит."""
        return self.__credit_used
    
    @property
    def available_credit(self) -> float:
        """Доступный кредит."""
        return self.__credit_limit - self.__credit_used
    
    # Переопределенный метод withdraw (с учетом кредитного лимита)
    def withdraw(self, amount: float, description: str = "Снятие со счета") -> dict:
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
        
        # Если на балансе достаточно средств
        if amount <= self.balance:
            self._BankAccount__balance -= amount
            return self._add_transaction("WITHDRAWAL", amount, description)
        
        # Если не хватает - используем кредит
        needed_credit = amount - self.balance
        
        if needed_credit > self.available_credit:
            raise ValueError(f"Превышение кредитного лимита. "
                           f"Доступно: {self.available_credit:.2f} {self.currency}")
        
        # Снимаем остаток с баланса
        if self.balance > 0:
            self._BankAccount__balance = 0
        
        # Увеличиваем использованный кредит
        self.__credit_used += needed_credit
        self._BankAccount__balance -= needed_credit
        
        self._add_transaction("CREDIT_USED", needed_credit, 
                             f"Использование кредита: {description}")
        
        return self._add_transaction("WITHDRAWAL", amount, description)
    
    # Переопределенный метод deposit (сначала погашает кредит)
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
        
        remaining = amount
        
        # Сначала погашаем кредит
        if self.__credit_used > 0:
            to_credit = min(remaining, self.__credit_used)
            self.__credit_used -= to_credit
            remaining -= to_credit
            self._add_transaction("CREDIT_REPAYMENT", to_credit, 
                                 f"Погашение кредита: {description}")
        
        # Остаток идет на баланс
        if remaining > 0:
            self._BankAccount__balance += remaining
        
        return self._add_transaction("DEPOSIT", amount, description)
    
    # Новый метод 1
    def get_debt(self) -> float:
        """Получение текущей задолженности."""
        return self.__credit_used
    
    # Новый метод 2
    def can_borrow(self, amount: float) -> bool:
        """Проверка, можно ли взять в кредит указанную сумму."""
        return amount <= self.available_credit
    
    # Переопределенный метод
    def calculate_annual_income(self) -> float:
        """Для кредитного счета доход отрицательный (расходы)."""
        return -self.__credit_used * 0.15  # 15% годовых
    
    def __str__(self) -> str:
        base_str = super().__str__()
        balance_str = f"{self.balance:,.2f}" if self.balance >= 0 else f"({abs(self.balance):,.2f})"
        return (base_str + f"\n   💳 Тип: Кредитный счет\n"
                f"   💳 Кредитный лимит: {self.__credit_limit:>12,.2f} {self.currency}\n"
                f"   📊 Использовано кредита: {self.__credit_used:>9,.2f} {self.currency}\n"
                f"   🟢 Доступно: {self.available_credit:>12,.2f} {self.currency}\n"
                f"   📍 Реальный баланс: {balance_str} {self.currency}")
    
    def __repr__(self) -> str:
        return (f"CreditAccount(owner_name='{self.owner_name}', "
                f"currency='{self.currency}', "
                f"balance={self.balance:.2f}, "
                f"credit_limit={self.__credit_limit})")