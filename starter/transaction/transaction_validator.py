# transaction_validator.py

from transaction.transaction_category import TransactionCategory


class ITransactionValidator:
    """Interface for transaction validation strategies (Strategy Pattern)."""

    def validate(self, transaction, current_balance):
        """
        Validate if a transaction can be applied.

        Args:
            transaction (Transaction): The transaction to validate.
            current_balance (float): The current balance before applying the transaction.

        Returns:
            tuple: (bool, str) - (is_valid, error_message)
        """
        raise NotImplementedError("Subclasses must implement validate method.")


class PermissiveValidator(ITransactionValidator):
    """Allow all transactions (default behavior)."""

    def validate(self, transaction, current_balance):
        """
        Allow all transactions without restrictions.

        Args:
            transaction (Transaction): The transaction to validate.
            current_balance (float): The current balance before applying the transaction.

        Returns:
            tuple: (True, None) - Always allows transactions.
        """
        return True, None


class StrictValidator(ITransactionValidator):
    """Prevent transactions that would make balance negative."""

    def validate(self, transaction, current_balance):
        """
        Validate that expenses don't cause negative balance.

        Args:
            transaction (Transaction): The transaction to validate.
            current_balance (float): The current balance before applying the transaction.

        Returns:
            tuple: (bool, str) - (is_valid, error_message if invalid)
        """
        if transaction.category == TransactionCategory.EXPENSE:
            new_balance = current_balance - transaction.amount
            if new_balance < 0:
                return False, f"Transaction rejected: Would result in negative balance (${new_balance:.2f})"
        return True, None


class LimitValidator(ITransactionValidator):
    """Enforce transaction amount limits."""

    def __init__(self, max_expense=None, max_income=None):
        """
        Initialize the limit validator with maximum transaction amounts.

        Args:
            max_expense (float, optional): Maximum allowed expense amount.
            max_income (float, optional): Maximum allowed income amount.
        """
        self.max_expense = max_expense
        self.max_income = max_income

    def validate(self, transaction, current_balance):
        """
        Validate that transaction amounts don't exceed limits.

        Args:
            transaction (Transaction): The transaction to validate.
            current_balance (float): The current balance before applying the transaction.

        Returns:
            tuple: (bool, str) - (is_valid, error_message if invalid)
        """
        if transaction.category == TransactionCategory.EXPENSE and self.max_expense is not None:
            if transaction.amount > self.max_expense:
                return False, f"Transaction rejected: Expense ${transaction.amount:.2f} exceeds limit ${self.max_expense:.2f}"

        if transaction.category == TransactionCategory.INCOME and self.max_income is not None:
            if transaction.amount > self.max_income:
                return False, f"Transaction rejected: Income ${transaction.amount:.2f} exceeds limit ${self.max_income:.2f}"

        return True, None


class CompositeValidator(ITransactionValidator):
    """Combine multiple validation strategies."""

    def __init__(self, validators):
        """
        Initialize the composite validator with multiple validators.

        Args:
            validators (list): List of ITransactionValidator instances.
        """
        self.validators = validators

    def validate(self, transaction, current_balance):
        """
        Validate transaction against all registered validators.

        Args:
            transaction (Transaction): The transaction to validate.
            current_balance (float): The current balance before applying the transaction.

        Returns:
            tuple: (bool, str) - (is_valid, error_message if any validator fails)
        """
        for validator in self.validators:
            is_valid, error_message = validator.validate(transaction, current_balance)
            if not is_valid:
                return False, error_message
        return True, None

