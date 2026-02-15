# balance.py

from transaction.transaction_category import TransactionCategory
from transaction.transaction_validator import PermissiveValidator

class Balance:
    """Singleton to track the balance."""

    _instance = None

    def __new__(cls):
        """
        Create or return the single instance of Balance.

        Returns:
            Balance: The single instance of the Balance class.
        """
        if cls._instance is None:
            cls._instance = super(Balance, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """Initialize the balance. Prevent direct instantiation."""
        if self._initialized:
            return

        self._net_balance = 0
        self._observers = []
        self._validator = PermissiveValidator()  # Default validator (Strategy Pattern)
        self._initialized = True

    @classmethod
    def get_instance(cls):
        """
        Get the singleton instance of Balance.

        Returns:
            Balance: The single instance of the Balance class.
        """
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def reset(self):
        """Reset the net balance to zero."""
        self._net_balance = 0

    def set_validator(self, validator):
        """
        Set the transaction validation strategy (Strategy Pattern).

        Args:
            validator (ITransactionValidator): The validator to use for transaction validation.
        """
        self._validator = validator

    def register_observer(self, observer):
        """
        Register an observer to be notified of balance changes.

        Args:
            observer (IBalanceObserver): The observer to register.
        """
        if observer not in self._observers:
            self._observers.append(observer)

    def unregister_observer(self, observer):
        """
        Unregister an observer from balance change notifications.

        Args:
            observer (IBalanceObserver): The observer to unregister.
        """
        if observer in self._observers:
            self._observers.remove(observer)

    def _notify_observers(self, transaction):
        """
        Notify all registered observers of a balance change.

        Args:
            transaction (Transaction): The transaction that triggered the update.
        """
        for observer in self._observers:
            observer.update(self, transaction)

    def add_income(self, amount):
        """
        Add income to the balance.

        Args:
            amount (float): The income amount to add.
        """
        self._net_balance += amount

    def add_expense(self, amount):
        """
        Subtract expense from the balance.

        Args:
            amount (float): The expense amount to subtract.
        """
        self._net_balance -= amount

    def apply_transaction(self, transaction):
        """
        Apply a Transaction object to update the balance.

        Args:
            transaction (Transaction): The transaction to apply.

        Raises:
            ValueError: If the transaction category is invalid or validation fails.
        """
        # Validate transaction using the current strategy
        is_valid, error_message = self._validator.validate(transaction, self._net_balance)
        if not is_valid:
            print(f"❌ {error_message}")
            return  # Don't apply invalid transactions

        if transaction.category == TransactionCategory.INCOME:
            self.add_income(transaction.amount)
        elif transaction.category == TransactionCategory.EXPENSE:
            self.add_expense(transaction.amount)
        else:
            raise ValueError(f"Invalid transaction category: {transaction.category}")

        self._notify_observers(transaction)

    def get_balance(self):
        """
        Get the current net balance.

        Returns:
            float: The current net balance.
        """
        return self._net_balance

    def summary(self):
        """
        Return a summary string of the net balance.

        Returns:
            str: A summary of the current balance.
        """
        return f"Net balance: ${self._net_balance:.2f}"

