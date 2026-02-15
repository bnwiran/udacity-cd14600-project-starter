import pytest

from balance.balance import Balance
from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory


@pytest.fixture
def balance():
    """Fixture that provides a clean Balance instance for each test."""
    balance_instance = Balance.get_instance()
    balance_instance.reset()
    balance_instance._observers = []
    yield balance_instance
    balance_instance._observers = []


def test_initial_balance(balance):
    """Test that initial balance is zero."""
    assert balance.get_balance() == 0.0


def test_singleton_instance():
    """Test that Balance is a singleton."""
    balance1 = Balance.get_instance()
    balance2 = Balance.get_instance()
    assert balance1 is balance2


def test_add_income(balance):
    """Test adding income increases balance."""
    balance.add_income(100)
    assert balance.get_balance() == 100


def test_add_income_multiple_times(balance):
    """Test adding multiple income transactions."""
    balance.add_income(100)
    balance.add_income(50)
    balance.add_income(25)
    assert balance.get_balance() == 175


def test_add_expense(balance):
    """Test adding expense decreases balance."""
    balance.add_expense(40)
    assert balance.get_balance() == -40


def test_add_expense_multiple_times(balance):
    """Test adding multiple expense transactions."""
    balance.add_expense(40)
    balance.add_expense(20)
    balance.add_expense(10)
    assert balance.get_balance() == -70


def test_combined_income_and_expense(balance):
    """Test combined income and expense transactions."""
    balance.add_income(100)
    balance.add_expense(30)
    balance.add_income(50)
    balance.add_expense(20)
    assert balance.get_balance() == 100


def test_apply_transaction_income(balance):
    """Test applying an income transaction."""
    t = Transaction(150, TransactionCategory.INCOME)
    balance.apply_transaction(t)
    assert balance.get_balance() == 150


def test_apply_transaction_expense(balance):
    """Test applying an expense transaction."""
    t = Transaction(60, TransactionCategory.EXPENSE)
    balance.apply_transaction(t)
    assert balance.get_balance() == -60


def test_apply_multiple_transactions(balance):
    """Test applying multiple transactions."""
    balance.apply_transaction(Transaction(200, TransactionCategory.INCOME))
    balance.apply_transaction(Transaction(75, TransactionCategory.EXPENSE))
    balance.apply_transaction(Transaction(100, TransactionCategory.INCOME))
    assert balance.get_balance() == 225


def test_apply_transaction_invalid_category(balance):
    """Test that invalid category raises ValueError."""

    class FakeCategory:
        pass

    t = Transaction(100, FakeCategory())
    with pytest.raises(ValueError):
        balance.apply_transaction(t)


def test_reset(balance):
    """Test resetting balance to zero."""
    balance.add_income(100)
    balance.add_expense(50)
    balance.reset()
    assert balance.get_balance() == 0.0


def test_reset_clears_negative_balance(balance):
    """Test resetting from negative balance."""
    balance.add_expense(100)
    assert balance.get_balance() == -100
    balance.reset()
    assert balance.get_balance() == 0.0


def test_summary_method(balance):
    """Test the summary method returns correct format."""
    balance.add_income(100)
    summary = balance.summary()
    assert summary == "Net balance: $100.00"


def test_summary_with_decimal(balance):
    """Test summary with decimal amounts."""
    balance.add_income(100.50)
    balance.add_expense(25.25)
    summary = balance.summary()
    assert summary == "Net balance: $75.25"


def test_fractional_amounts(balance):
    """Test handling fractional currency amounts."""
    balance.add_income(99.99)
    balance.add_expense(49.50)
    assert balance.get_balance() == pytest.approx(50.49, abs=0.01)
