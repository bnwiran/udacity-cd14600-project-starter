# test_transaction_validator.py

import pytest
from balance.balance import Balance
from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory
from transaction.transaction_validator import (
    ITransactionValidator,
    PermissiveValidator,
    StrictValidator,
    LimitValidator,
    CompositeValidator
)


class TestITransactionValidator:
    """Test the ITransactionValidator interface."""

    def test_interface_raises_not_implemented(self):
        """Test that the interface method raises NotImplementedError."""
        validator = ITransactionValidator()
        transaction = Transaction(100, TransactionCategory.INCOME)
        with pytest.raises(NotImplementedError):
            validator.validate(transaction, 0)


class TestPermissiveValidator:
    """Test the PermissiveValidator strategy."""

    def test_allows_all_income_transactions(self):
        """Test that all income transactions are allowed."""
        validator = PermissiveValidator()
        transaction = Transaction(1000, TransactionCategory.INCOME)
        is_valid, error = validator.validate(transaction, 0)
        assert is_valid is True
        assert error is None

    def test_allows_all_expense_transactions(self):
        """Test that all expense transactions are allowed."""
        validator = PermissiveValidator()
        transaction = Transaction(1000, TransactionCategory.EXPENSE)
        is_valid, error = validator.validate(transaction, 0)
        assert is_valid is True
        assert error is None

    def test_allows_transactions_causing_negative_balance(self):
        """Test that transactions causing negative balance are allowed."""
        validator = PermissiveValidator()
        transaction = Transaction(500, TransactionCategory.EXPENSE)
        is_valid, error = validator.validate(transaction, 100)
        assert is_valid is True
        assert error is None


class TestStrictValidator:
    """Test the StrictValidator strategy."""

    def test_allows_income_transactions(self):
        """Test that income transactions are always allowed."""
        validator = StrictValidator()
        transaction = Transaction(1000, TransactionCategory.INCOME)
        is_valid, error = validator.validate(transaction, 0)
        assert is_valid is True
        assert error is None

    def test_allows_expense_with_sufficient_balance(self):
        """Test that expense transactions are allowed with sufficient balance."""
        validator = StrictValidator()
        transaction = Transaction(50, TransactionCategory.EXPENSE)
        is_valid, error = validator.validate(transaction, 100)
        assert is_valid is True
        assert error is None

    def test_rejects_expense_causing_negative_balance(self):
        """Test that expense transactions causing negative balance are rejected."""
        validator = StrictValidator()
        transaction = Transaction(200, TransactionCategory.EXPENSE)
        is_valid, error = validator.validate(transaction, 100)
        assert is_valid is False
        assert "negative balance" in error.lower()
        assert "-100.00" in error

    def test_allows_expense_exactly_at_balance(self):
        """Test that expense equal to current balance is allowed."""
        validator = StrictValidator()
        transaction = Transaction(100, TransactionCategory.EXPENSE)
        is_valid, error = validator.validate(transaction, 100)
        assert is_valid is True
        assert error is None


class TestLimitValidator:
    """Test the LimitValidator strategy."""

    def test_allows_expense_within_limit(self):
        """Test that expense within limit is allowed."""
        validator = LimitValidator(max_expense=100)
        transaction = Transaction(75, TransactionCategory.EXPENSE)
        is_valid, error = validator.validate(transaction, 200)
        assert is_valid is True
        assert error is None

    def test_rejects_expense_exceeding_limit(self):
        """Test that expense exceeding limit is rejected."""
        validator = LimitValidator(max_expense=100)
        transaction = Transaction(150, TransactionCategory.EXPENSE)
        is_valid, error = validator.validate(transaction, 200)
        assert is_valid is False
        assert "exceeds limit" in error.lower()
        assert "150.00" in error
        assert "100.00" in error

    def test_allows_expense_exactly_at_limit(self):
        """Test that expense exactly at limit is allowed."""
        validator = LimitValidator(max_expense=100)
        transaction = Transaction(100, TransactionCategory.EXPENSE)
        is_valid, error = validator.validate(transaction, 200)
        assert is_valid is True
        assert error is None

    def test_allows_income_within_limit(self):
        """Test that income within limit is allowed."""
        validator = LimitValidator(max_income=1000)
        transaction = Transaction(500, TransactionCategory.INCOME)
        is_valid, error = validator.validate(transaction, 100)
        assert is_valid is True
        assert error is None

    def test_rejects_income_exceeding_limit(self):
        """Test that income exceeding limit is rejected."""
        validator = LimitValidator(max_income=1000)
        transaction = Transaction(1500, TransactionCategory.INCOME)
        is_valid, error = validator.validate(transaction, 100)
        assert is_valid is False
        assert "exceeds limit" in error.lower()

    def test_allows_all_when_no_limits_set(self):
        """Test that all transactions are allowed when no limits are set."""
        validator = LimitValidator()
        expense = Transaction(10000, TransactionCategory.EXPENSE)
        income = Transaction(10000, TransactionCategory.INCOME)
        assert validator.validate(expense, 100)[0] is True
        assert validator.validate(income, 100)[0] is True

    def test_expense_limit_only(self):
        """Test validator with expense limit only."""
        validator = LimitValidator(max_expense=50)
        expense_ok = Transaction(30, TransactionCategory.EXPENSE)
        expense_bad = Transaction(100, TransactionCategory.EXPENSE)
        income_large = Transaction(10000, TransactionCategory.INCOME)

        assert validator.validate(expense_ok, 100)[0] is True
        assert validator.validate(expense_bad, 100)[0] is False
        assert validator.validate(income_large, 100)[0] is True

    def test_income_limit_only(self):
        """Test validator with income limit only."""
        validator = LimitValidator(max_income=500)
        income_ok = Transaction(300, TransactionCategory.INCOME)
        income_bad = Transaction(1000, TransactionCategory.INCOME)
        expense_large = Transaction(10000, TransactionCategory.EXPENSE)

        assert validator.validate(income_ok, 100)[0] is True
        assert validator.validate(income_bad, 100)[0] is False
        assert validator.validate(expense_large, 100)[0] is True


class TestCompositeValidator:
    """Test the CompositeValidator strategy."""

    def test_passes_when_all_validators_pass(self):
        """Test that transaction is allowed when all validators pass."""
        composite = CompositeValidator([
            StrictValidator(),
            LimitValidator(max_expense=100)
        ])
        transaction = Transaction(50, TransactionCategory.EXPENSE)
        is_valid, error = composite.validate(transaction, 200)
        assert is_valid is True
        assert error is None

    def test_fails_when_any_validator_fails(self):
        """Test that transaction is rejected when any validator fails."""
        composite = CompositeValidator([
            StrictValidator(),
            LimitValidator(max_expense=100)
        ])
        transaction = Transaction(150, TransactionCategory.EXPENSE)
        is_valid, error = composite.validate(transaction, 200)
        assert is_valid is False
        assert error is not None

    def test_fails_on_first_failed_validator(self):
        """Test that validation stops at first failed validator."""
        composite = CompositeValidator([
            LimitValidator(max_expense=50),
            StrictValidator()
        ])
        transaction = Transaction(100, TransactionCategory.EXPENSE)
        is_valid, error = composite.validate(transaction, 200)
        assert is_valid is False
        assert "exceeds limit" in error.lower()  # Should fail on first validator

    def test_empty_validator_list_allows_all(self):
        """Test that empty validator list allows all transactions."""
        composite = CompositeValidator([])
        transaction = Transaction(1000, TransactionCategory.EXPENSE)
        is_valid, error = composite.validate(transaction, 0)
        assert is_valid is True
        assert error is None

    def test_three_validators_combined(self):
        """Test combining three validators."""
        composite = CompositeValidator([
            PermissiveValidator(),
            StrictValidator(),
            LimitValidator(max_expense=100)
        ])
        # Should pass all three
        transaction_ok = Transaction(50, TransactionCategory.EXPENSE)
        is_valid, error = composite.validate(transaction_ok, 200)
        assert is_valid is True

        # Should fail on LimitValidator
        transaction_bad = Transaction(150, TransactionCategory.EXPENSE)
        is_valid, error = composite.validate(transaction_bad, 200)
        assert is_valid is False


class TestBalanceWithValidators:
    """Test Balance class integration with validators."""

    def setup_method(self):
        """Reset balance before each test."""
        balance = Balance.get_instance()
        balance.reset()

    def test_balance_uses_default_permissive_validator(self):
        """Test that Balance uses PermissiveValidator by default."""
        balance = Balance.get_instance()
        balance.reset()

        # Should allow transaction that would cause negative balance
        balance.apply_transaction(Transaction(100, TransactionCategory.INCOME))
        balance.apply_transaction(Transaction(200, TransactionCategory.EXPENSE))

        assert balance.get_balance() == -100

    def test_balance_can_change_validator_strategy(self):
        """Test that Balance can dynamically change validation strategy."""
        balance = Balance.get_instance()
        balance.reset()

        # Start with permissive
        balance.apply_transaction(Transaction(100, TransactionCategory.INCOME))
        assert balance.get_balance() == 100

        # Switch to strict
        balance.set_validator(StrictValidator())
        balance.apply_transaction(Transaction(50, TransactionCategory.EXPENSE))
        assert balance.get_balance() == 50

        # This should be rejected by StrictValidator
        balance.apply_transaction(Transaction(200, TransactionCategory.EXPENSE))
        assert balance.get_balance() == 50  # Balance unchanged

    def test_balance_with_limit_validator(self):
        """Test Balance with LimitValidator strategy."""
        balance = Balance.get_instance()
        balance.reset()
        balance.set_validator(LimitValidator(max_expense=100))

        balance.apply_transaction(Transaction(500, TransactionCategory.INCOME))
        balance.apply_transaction(Transaction(75, TransactionCategory.EXPENSE))

        # This should be rejected
        balance.apply_transaction(Transaction(150, TransactionCategory.EXPENSE))

        assert balance.get_balance() == 425  # 500 - 75

    def test_balance_with_composite_validator(self):
        """Test Balance with CompositeValidator strategy."""
        balance = Balance.get_instance()
        balance.reset()
        composite = CompositeValidator([
            StrictValidator(),
            LimitValidator(max_expense=100)
        ])
        balance.set_validator(composite)

        balance.apply_transaction(Transaction(200, TransactionCategory.INCOME))
        balance.apply_transaction(Transaction(50, TransactionCategory.EXPENSE))

        # Should be rejected by LimitValidator
        balance.apply_transaction(Transaction(150, TransactionCategory.EXPENSE))

        # Should be rejected by StrictValidator
        balance.apply_transaction(Transaction(120, TransactionCategory.EXPENSE))

        assert balance.get_balance() == 150  # 200 - 50

