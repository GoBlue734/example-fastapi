import pytest
from app.calculations import add, subtract, multiply, divide, BankAccount, InsufficientFunds

@pytest.fixture
def zero_bank_account():
    return BankAccount()


@pytest.fixture
def bank_account():
    return BankAccount(50)


# Values for testing add function
@pytest.mark.parametrize("num1, num2, expected", [
    (5, 3, 8),
    (5, -3, 2),
    (-5, 3, -2),
    (-5, -3, -8),
    (5.0, 3.0, 8.0),
    (5.5, 3.5, 9.0),
    (5.0, -3.0, 2.0),
    (-5.0, 3.0, -2.0),
    (-5.0, -3.0, -8.0),
    (5.5, -3.5, 2.0),
    (-5.5, 3.5, -2.0),
    (-5.5, -3.5, -9.0),
])

def test_add(num1, num2, expected):
    print("Testing add function")
    assert add(num1, num2) == expected

# Values for testing subtract function
@pytest.mark.parametrize("num3, num4, expected", [
    (5, 3, 2),
    (5, -3, 8),
    (-5, 3, -8),
    (-5, -3, -2),
    (5.0, 3.0, 2.0),
    (5.5, 3.5, 2.0),
    (5.0, -3.0, 8.0),
    (-5.0, 3.0, -8.0),
    (-5.0, -3.0, -2.0),
    (5.5, -3.5, 9.0),
    (-5.5, 3.5, -9.0),
    (-5.5, -3.5, -2.0),
])

def test_subtract(num3, num4, expected):
    print("Testing subtract function")
    assert subtract(num3, num4) == expected

# Values for testing multiply function
@pytest.mark.parametrize("num5, num6, expected", [
    (5, 3, 15),
    (5, -3, -15),
    (-5, 3, -15),
    (-5, -3, 15),
    (5.0, 3.0, 15.0),
    (5.5, 3.5, 19.25),
    (5.0, -3.0, -15.0),
    (-5.0, 3.0, -15.0),
    (-5.0, -3.0, 15.0),
    (5.5, -3.5, -19.25),
    (-5.5, 3.5, -19.25),
    (-5.5, -3.5, 19.25),
])

def test_multiply(num5, num6, expected):
    print("Testing multiply function")
    assert multiply(num5, num6) == expected

# Values for testing divide function
@pytest.mark.parametrize("num7, num8, expected", [
    (15, 3, 5),
    (15, -3, -5),
    (-15, 3, -5),
    (-15, -3, 5),
    (15.0, 3.0, 5.0),
    (15.0, -3.0, -5.0),
    (-15.0, 3.0, -5.0),
    (-15.0, -3.0, 5.0),
])

def test_divide(num7, num8, expected):
    print("Testing divide function")
    assert divide(num7, num8) == expected

def test_bank_set_initial_amount(bank_account):
    assert bank_account.balance == 50

def test_bank_default_amount(zero_bank_account):
    assert zero_bank_account.balance == 0


def test_withdraw(bank_account):
    bank_account.withdraw(20)
    assert bank_account.balance == 30


def test_deposit(bank_account):
    bank_account.deposit(30)
    assert bank_account.balance == 80

def test_collect_interest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance, 6) == 55

@pytest.mark.parametrize("deposited, withdrew, expected", [
    (200, 100, 100),
    (50, 10, 40),
    (1200, 200, 1000)
])

def test_bank_transaction(zero_bank_account, deposited, withdrew, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == expected

def test_insufficient_funds(bank_account):
    with pytest.raises(Exception):
        bank_account.withdraw(200)