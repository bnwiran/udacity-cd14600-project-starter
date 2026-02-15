from transaction.external_income_transaction import ExternalFreelanceIncome
from transaction.transaction import Transaction
from transaction.transaction_adapter import TransactionAdapter
from transaction.transaction_category import TransactionCategory


class TestTransactionAdapter:
    """Test suite for TransactionAdapter class."""

    def test_adapter_converts_freelance_income_object(self):
        """Test adapter converts ExternalFreelanceIncome object to Transaction."""
        ext_txn = ExternalFreelanceIncome(500, "INV-12345", "Website development")
        adapter = TransactionAdapter(ext_txn)
        txn = adapter.to_transaction()

        assert txn.amount == 500
        assert txn.category == TransactionCategory.INCOME

    def test_adapter_converts_dict_with_income(self):
        """Test adapter converts dict with income category."""
        ext_txn = {'amount': 300, 'category': 'INCOME'}
        adapter = TransactionAdapter(ext_txn)
        txn = adapter.to_transaction()

        assert txn.amount == 300
        assert txn.category == TransactionCategory.INCOME

    def test_adapter_converts_dict_with_expense(self):
        """Test adapter converts dict with expense category."""
        ext_txn = {'amount': 75, 'category': 'EXPENSE'}
        adapter = TransactionAdapter(ext_txn)
        txn = adapter.to_transaction()

        assert txn.amount == 75
        assert txn.category == TransactionCategory.EXPENSE

    def test_adapter_converts_dict_missing_category(self):
        """Test adapter handles dict with missing category (defaults to INCOME)."""
        ext_txn = {'amount': 100}
        adapter = TransactionAdapter(ext_txn)
        txn = adapter.to_transaction()

        assert txn.amount == 100
        assert txn.category == TransactionCategory.INCOME

    def test_adapter_converts_dict_invalid_category(self):
        """Test adapter handles dict with invalid category (defaults to INCOME)."""
        ext_txn = {'amount': 200, 'category': 'INVALID'}
        adapter = TransactionAdapter(ext_txn)
        txn = adapter.to_transaction()

        assert txn.amount == 200
        assert txn.category == TransactionCategory.INCOME

    def test_adapter_with_float_amount(self):
        """Test adapter handles float amounts."""
        ext_txn = {'amount': 99.99, 'category': 'INCOME'}
        adapter = TransactionAdapter(ext_txn)
        txn = adapter.to_transaction()

        assert txn.amount == 99.99

    def test_adapter_with_zero_amount(self):
        """Test adapter handles zero amount."""
        ext_txn = {'amount': 0, 'category': 'EXPENSE'}
        adapter = TransactionAdapter(ext_txn)
        txn = adapter.to_transaction()

        assert txn.amount == 0

    def test_adapter_result_is_transaction(self):
        """Test that adapter returns a Transaction object."""
        ext_txn = {'amount': 100, 'category': 'INCOME'}
        adapter = TransactionAdapter(ext_txn)
        txn = adapter.to_transaction()

        assert isinstance(txn, Transaction)

    def test_adapter_equality_of_converted_transactions(self):
        """Test that converted transactions can be compared for equality."""
        ext_txn1 = {'amount': 500, 'category': 'INCOME'}
        ext_txn2 = {'amount': 500, 'category': 'INCOME'}

        adapter1 = TransactionAdapter(ext_txn1)
        adapter2 = TransactionAdapter(ext_txn2)

        txn1 = adapter1.to_transaction()
        txn2 = adapter2.to_transaction()

        assert txn1 == txn2

    def test_adapter_freelance_income_with_different_amounts(self):
        """Test adapter with different freelance income amounts."""
        amounts = [250, 500, 1000, 99.99]

        for amount in amounts:
            ext_txn = ExternalFreelanceIncome(amount, "INV-001", "Work")
            adapter = TransactionAdapter(ext_txn)
            txn = adapter.to_transaction()

            assert txn.amount == amount
            assert txn.category == TransactionCategory.INCOME

    def test_adapter_preserves_amount_precision(self):
        """Test that adapter preserves decimal precision."""
        ext_txn = {'amount': 123.456789, 'category': 'INCOME'}
        adapter = TransactionAdapter(ext_txn)
        txn = adapter.to_transaction()

        assert txn.amount == 123.456789

    def test_adapter_case_insensitive_category(self):
        """Test that adapter handles category case insensitively."""
        categories = ['income', 'INCOME', 'Income', 'INCome']

        for category in categories:
            ext_txn = {'amount': 100, 'category': category.upper()}
            adapter = TransactionAdapter(ext_txn)
            txn = adapter.to_transaction()

            assert txn.category == TransactionCategory.INCOME

    def test_adapter_with_negative_amount(self):
        """Test adapter handles negative amounts."""
        ext_txn = {'amount': -50, 'category': 'INCOME'}
        adapter = TransactionAdapter(ext_txn)
        txn = adapter.to_transaction()

        assert txn.amount == -50
