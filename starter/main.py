"""This module serves as the entry point for the program."""
from balance.balance import Balance
from balance.balance_observer import LowBalanceAlertObserver
from balance.balance_observer import PrintObserver
from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory
from transaction.transaction_adapter import TransactionAdapter
from transaction.external_income_transaction import ExternalFreelanceIncome
from transaction.transaction_validator import (
    PermissiveValidator,
    StrictValidator,
    LimitValidator,
    CompositeValidator
)


def main():
    print("=" * 60)
    print("DEMONSTRATION: Strategy Pattern for Transaction Validation")
    print("=" * 60)

    # Create balance and add observers
    balance = Balance.get_instance()
    balance.reset()  # Reset to start fresh

    # Add observers
    print_observer = PrintObserver()
    low_balance_observer = LowBalanceAlertObserver(threshold=100)

    balance.register_observer(print_observer)
    balance.register_observer(low_balance_observer)

    # Create standard transactions
    transactions = [
        Transaction(100, TransactionCategory.INCOME),
        Transaction(50, TransactionCategory.EXPENSE),
        Transaction(200, TransactionCategory.INCOME),
        Transaction(75, TransactionCategory.EXPENSE),
    ]

    # Create an external income transaction (via Adapter pattern)
    freelance_income = ExternalFreelanceIncome(1200, "INV-98765", "Mobile App Project")
    adapter = TransactionAdapter(freelance_income)
    adapted_transaction = adapter.to_transaction()

    all_transactions = transactions + [adapted_transaction]

    # DEMO 1: Using PermissiveValidator (default - allows all transactions)
    print("\n--- STRATEGY 1: Permissive Validator (Default) ---")
    print("Allows all transactions without restrictions.\n")
    balance.set_validator(PermissiveValidator())

    for transaction in all_transactions:
        balance.apply_transaction(transaction)

    print(f"\n{balance.summary()}")

    # DEMO 2: Using StrictValidator (prevents negative balance)
    print("\n\n--- STRATEGY 2: Strict Validator ---")
    print("Prevents transactions that would cause negative balance.\n")
    balance.reset()
    balance.set_validator(StrictValidator())

    # Add some transactions including one that would go negative
    demo_transactions = [
        Transaction(100, TransactionCategory.INCOME),
        Transaction(50, TransactionCategory.EXPENSE),
        Transaction(200, TransactionCategory.EXPENSE),  # This should be rejected (100-50-200 = -150)
        Transaction(30, TransactionCategory.EXPENSE),   # This should succeed
    ]

    for transaction in demo_transactions:
        balance.apply_transaction(transaction)

    print(f"\n{balance.summary()}")

    # DEMO 3: Using LimitValidator (enforce transaction limits)
    print("\n\n--- STRATEGY 3: Limit Validator ---")
    print("Enforces maximum expense limit of $100.\n")
    balance.reset()
    balance.set_validator(LimitValidator(max_expense=100))

    limit_transactions = [
        Transaction(500, TransactionCategory.INCOME),
        Transaction(75, TransactionCategory.EXPENSE),   # Should succeed
        Transaction(150, TransactionCategory.EXPENSE),  # Should be rejected (exceeds $100 limit)
        Transaction(50, TransactionCategory.EXPENSE),   # Should succeed
    ]

    for transaction in limit_transactions:
        balance.apply_transaction(transaction)

    print(f"\n{balance.summary()}")

    # DEMO 4: Using CompositeValidator (combine multiple strategies)
    print("\n\n--- STRATEGY 4: Composite Validator ---")
    print("Combines Strict + Limit validators (no negative balance AND max $100 expense).\n")
    balance.reset()
    composite = CompositeValidator([
        StrictValidator(),
        LimitValidator(max_expense=100)
    ])
    balance.set_validator(composite)

    composite_transactions = [
        Transaction(200, TransactionCategory.INCOME),
        Transaction(75, TransactionCategory.EXPENSE),   # Should succeed
        Transaction(150, TransactionCategory.EXPENSE),  # Should be rejected (exceeds limit)
        Transaction(50, TransactionCategory.EXPENSE),   # Should succeed
        Transaction(100, TransactionCategory.EXPENSE),  # Should be rejected (would go negative: 200-75-50-100 = -25)
    ]

    for transaction in composite_transactions:
        balance.apply_transaction(transaction)

    print(f"\n{balance.summary()}")
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
