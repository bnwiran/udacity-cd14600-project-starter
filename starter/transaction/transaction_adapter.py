# transaction_adapter.py

from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory

class TransactionAdapter:
    """Adapter to convert external transaction formats to standard Transaction objects."""

    def __init__(self, external_transaction):
        """
        Initialize the adapter with an external transaction.

        Args:
            external_transaction: Either a dict or an object with amount and typ attributes.
        """
        self.external_transaction = external_transaction

    def to_transaction(self):
        """
        Convert an external transaction to a standard Transaction.

        Returns:
            Transaction: The converted transaction object.
        """
        if isinstance(self.external_transaction, dict):
            amount = self.external_transaction.get('amount')
            category_str = self.external_transaction.get('category', 'OTHER')
        else:
            # Handle objects like ExternalFreelanceIncome
            amount = self.external_transaction.amount
            category_str = self.external_transaction.typ.upper() if hasattr(self.external_transaction, 'typ') else 'OTHER'

        category = TransactionCategory[category_str] if category_str in TransactionCategory.__members__ else TransactionCategory.INCOME
        return Transaction(
            amount=amount,
            category=category
        )
