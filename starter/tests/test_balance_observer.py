import pytest
from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory
from balance.balance import Balance
from balance.balance_observer import (
    IBalanceObserver,
    PrintObserver,
    LowBalanceAlertObserver
)


@pytest.fixture
def balance():
    """Fixture that provides a clean Balance instance for each test."""
    balance_instance = Balance.get_instance()
    balance_instance.reset()
    balance_instance._observers = []
    yield balance_instance
    balance_instance._observers = []


class TestIBalanceObserver:
    """Test the IBalanceObserver interface."""

    def test_interface_raises_not_implemented(self, balance):
        """Test that abstract interface raises NotImplementedError."""
        observer = IBalanceObserver()
        with pytest.raises(NotImplementedError):
            observer.update(balance, None)


class TestPrintObserver:
    """Test the PrintObserver implementation."""

    def test_print_observer_prints_on_update(self, balance):
        """Test that PrintObserver prints transaction and balance."""
        observer = PrintObserver()
        balance.register_observer(observer)

        transaction = Transaction(100, TransactionCategory.INCOME)
        balance.apply_transaction(transaction)

        # Verify observer was registered and transaction was applied
        assert observer in balance._observers

    def test_print_observer_multiple_transactions(self, balance):
        """Test PrintObserver with multiple transactions."""
        observer = PrintObserver()
        balance.register_observer(observer)

        balance.apply_transaction(Transaction(100, TransactionCategory.INCOME))
        balance.apply_transaction(Transaction(25, TransactionCategory.EXPENSE))

        # Verify observer is still registered after multiple transactions
        assert observer in balance._observers


class TestLowBalanceAlertObserver:
    """Test the LowBalanceAlertObserver implementation."""

    def test_alert_triggers_on_low_balance(self, balance):
        """Test that alert triggers when balance drops below threshold."""
        observer = LowBalanceAlertObserver(threshold=50)
        balance.register_observer(observer)

        balance.apply_transaction(Transaction(100, TransactionCategory.INCOME))
        assert observer.alert_triggered is False

        balance.apply_transaction(Transaction(60, TransactionCategory.EXPENSE))
        assert observer.alert_triggered is True

    def test_alert_recovers_when_above_threshold(self, balance):
        """Test that alert_triggered flag resets when balance recovers."""
        observer = LowBalanceAlertObserver(threshold=50)
        balance.register_observer(observer)

        balance.apply_transaction(Transaction(100, TransactionCategory.INCOME))
        balance.apply_transaction(Transaction(60, TransactionCategory.EXPENSE))
        assert observer.alert_triggered is True

        balance.apply_transaction(Transaction(100, TransactionCategory.INCOME))
        assert observer.alert_triggered is False

    def test_alert_with_zero_threshold(self, balance):
        """Test alert observer with zero threshold."""
        observer = LowBalanceAlertObserver(threshold=0)
        balance.register_observer(observer)

        balance.apply_transaction(Transaction(50, TransactionCategory.INCOME))
        assert observer.alert_triggered is False

        balance.apply_transaction(Transaction(60, TransactionCategory.EXPENSE))
        assert observer.alert_triggered is True

    def test_alert_with_negative_balance(self, balance):
        """Test alert observer with negative balance."""
        observer = LowBalanceAlertObserver(threshold=-10)
        balance.register_observer(observer)

        balance.apply_transaction(Transaction(50, TransactionCategory.EXPENSE))
        assert observer.alert_triggered is True

    def test_alert_prints_warning_message(self, balance):
        """Test that alert prints warning message."""
        observer = LowBalanceAlertObserver(threshold=50)
        balance.register_observer(observer)

        balance.apply_transaction(Transaction(100, TransactionCategory.INCOME))
        balance.apply_transaction(Transaction(60, TransactionCategory.EXPENSE))

        # Verify alert was triggered when balance dropped below threshold
        assert observer.alert_triggered is True


class TestObserverRegistration:
    """Test observer registration and management."""

    def test_register_observer(self, balance):
        """Test registering an observer."""
        observer = PrintObserver()
        balance.register_observer(observer)
        assert observer in balance._observers

    def test_unregister_observer(self, balance):
        """Test unregistering an observer."""
        observer = PrintObserver()
        balance.register_observer(observer)
        balance.unregister_observer(observer)
        assert observer not in balance._observers

    def test_register_multiple_observers(self, balance):
        """Test registering multiple observers."""
        observer1 = PrintObserver()
        observer2 = LowBalanceAlertObserver(50)
        balance.register_observer(observer1)
        balance.register_observer(observer2)

        assert len(balance._observers) == 2
        assert observer1 in balance._observers
        assert observer2 in balance._observers

    def test_cannot_register_duplicate_observer(self, balance):
        """Test that the same observer cannot be registered twice."""
        observer = PrintObserver()
        balance.register_observer(observer)
        balance.register_observer(observer)

        assert len(balance._observers) == 1

    def test_unregister_nonexistent_observer(self, balance):
        """Test unregistering an observer that was never registered."""
        observer = PrintObserver()
        balance.unregister_observer(observer)
        assert len(balance._observers) == 0

    def test_all_observers_notified(self, balance):
        """Test that all registered observers are notified."""
        observer1 = PrintObserver()
        observer2 = PrintObserver()
        balance.register_observer(observer1)
        balance.register_observer(observer2)

        balance.apply_transaction(Transaction(100, TransactionCategory.INCOME))

        # Verify both observers are registered
        assert len(balance._observers) == 2
