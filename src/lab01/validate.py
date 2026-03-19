def validate_owner(value):
    if not isinstance(value, str):
        raise TypeError("owner must be string")
    if not value.strip():
        raise ValueError("owner empty")
    return value.strip()


def validate_balance(value):
    if not isinstance(value, (int, float)):
        raise TypeError("balance must be number")
    if value < 0:
        raise ValueError("balance must be >=0")
    return value


def validate_account_number(value):
    if not isinstance(value, str):
        raise TypeError("account number must be string")
    if not value.strip():
        raise ValueError("account number empty")
    return value


def validate_credit_limit(value):
    if not isinstance(value, (int, float)):
        raise TypeError("credit limit must be number")
    if value < 0:
        raise ValueError("credit limit must be >=0")
    return value


def validate_interest_rate(value):
    if not isinstance(value, (int, float)):
        raise TypeError("interest rate must be number")
    if value < 0 or value > 100:
        raise ValueError("interest rate must be 0-100")
    return value


def validate_money(value):
    if not isinstance(value, (int, float)):
        raise TypeError("money must be number")
    if value <= 0:
        raise ValueError("money must be >0")
    return value