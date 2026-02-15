# transaction.py

from transaction.transaction_category import TransactionCategory

class Transaction:
    """Represents a financial transaction with an amount and category."""

    def __init__(self, amount, category: TransactionCategory):
        self.amount = amount
        self.category = category

    def __str__(self):
        """Return a string representation of the transaction."""
        return f"Transaction(${self.amount}, category='{self.category}')"

    def __eq__(self, other):
        """Check if two transactions are equal based on amount and category."""
        if not isinstance(other, Transaction):
            return False
        return self.amount == other.amount and self.category == other.category
