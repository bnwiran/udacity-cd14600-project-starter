# balance_observer.py

class IBalanceObserver:
    def update(self, balance, transaction):
        """Handle balance updates."""
        raise NotImplementedError("Subclasses must implement update method.")


class PrintObserver(IBalanceObserver):
    def update(self, balance, transaction):
        """Print balance update message."""
        print(f"Balance Update: {transaction} | New Balance: ${balance.get_balance():.2f}")


class LowBalanceAlertObserver(IBalanceObserver):
    def __init__(self, threshold):
        self.threshold = threshold
        self.alert_triggered = False

    def update(self, balance, transaction):
        """Alert if balance drops below threshold."""
        current_balance = balance.get_balance()
        if current_balance < self.threshold:
            print(f"⚠️ LOW BALANCE ALERT: Balance (${current_balance:.2f}) is below threshold (${self.threshold:.2f})")
            self.alert_triggered = True
        else:
            self.alert_triggered = False
