from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory


class TestTransaction:
    """Test suite for Transaction class."""

    def test_transaction_creation(self):
        """Test creating a transaction with amount and category."""
        t = Transaction(100, TransactionCategory.EXPENSE)
        assert t.amount == 100
        assert t.category == TransactionCategory.EXPENSE

    def test_transaction_creation_income(self):
        """Test creating an income transaction."""
        t = Transaction(500, TransactionCategory.INCOME)
        assert t.amount == 500
        assert t.category == TransactionCategory.INCOME

    def test_transaction_with_float_amount(self):
        """Test creating a transaction with float amount."""
        t = Transaction(99.99, TransactionCategory.EXPENSE)
        assert t.amount == 99.99

    def test_transaction_with_zero_amount(self):
        """Test creating a transaction with zero amount."""
        t = Transaction(0, TransactionCategory.INCOME)
        assert t.amount == 0

    def test_transaction_with_large_amount(self):
        """Test creating a transaction with large amount."""
        t = Transaction(1000000, TransactionCategory.INCOME)
        assert t.amount == 1000000

    def test_transaction_str_expense(self):
        """Test string representation of expense transaction."""
        t = Transaction(50, TransactionCategory.EXPENSE)
        assert "50" in str(t)
        assert "EXPENSE" in str(t)

    def test_transaction_str_income(self):
        """Test string representation of income transaction."""
        t = Transaction(100, TransactionCategory.INCOME)
        result = str(t)
        assert "100" in result
        assert "INCOME" in result

    def test_transaction_str_format(self):
        """Test that string representation includes Transaction label."""
        t = Transaction(75.50, TransactionCategory.EXPENSE)
        assert "Transaction" in str(t)
        assert "75.5" in str(t)

    def test_transaction_equality_same_values(self):
        """Test that two transactions with same values are equal."""
        t1 = Transaction(20, TransactionCategory.EXPENSE)
        t2 = Transaction(20, TransactionCategory.EXPENSE)
        assert t1 == t2

    def test_transaction_equality_different_amounts(self):
        """Test that transactions with different amounts are not equal."""
        t1 = Transaction(20, TransactionCategory.EXPENSE)
        t2 = Transaction(30, TransactionCategory.EXPENSE)
        assert t1 != t2

    def test_transaction_equality_different_categories(self):
        """Test that transactions with different categories are not equal."""
        t1 = Transaction(20, TransactionCategory.EXPENSE)
        t2 = Transaction(20, TransactionCategory.INCOME)
        assert t1 != t2

    def test_transaction_equality_both_different(self):
        """Test inequality when both amount and category differ."""
        t1 = Transaction(20, TransactionCategory.EXPENSE)
        t2 = Transaction(30, TransactionCategory.INCOME)
        assert t1 != t2

    def test_transaction_equality_with_non_transaction(self):
        """Test inequality when comparing with non-Transaction object."""
        t = Transaction(20, TransactionCategory.EXPENSE)
        assert t != 20
        assert t != "Transaction"
        assert t != None

    def test_transaction_not_equal_to_dict(self):
        """Test that Transaction is not equal to dict with same values."""
        t = Transaction(100, TransactionCategory.INCOME)
        d = {'amount': 100, 'category': TransactionCategory.INCOME}
        assert t != d

    def test_transaction_category_enum(self):
        """Test that transaction category is a TransactionCategory enum."""
        t = Transaction(50, TransactionCategory.INCOME)
        assert isinstance(t.category, TransactionCategory)

    def test_transaction_attributes_mutable(self):
        """Test that transaction attributes can be modified."""
        t = Transaction(50, TransactionCategory.INCOME)
        t.amount = 100
        assert t.amount == 100

    def test_multiple_transactions_independent(self):
        """Test that multiple transactions are independent."""
        t1 = Transaction(50, TransactionCategory.INCOME)
        t2 = Transaction(25, TransactionCategory.EXPENSE)

        assert t1.amount == 50
        assert t2.amount == 25
        assert t1 != t2

    def test_transaction_with_negative_amount(self):
        """Test creating a transaction with negative amount."""
        t = Transaction(-50, TransactionCategory.INCOME)
        assert t.amount == -50
