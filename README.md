# Personal Finance Manager — Design Patterns Project

This project is a hands-on exercise in applying Object-Oriented Design Patterns to build a simplified personal finance manager.
You will implement and extend starter code to add functionality such as tracking transactions, adapting external data, observing balance changes, and ensuring proper architectural patterns.

## Getting Started

### Dependencies

Make sure you have python version >= 3.10.x installed on your computer. 


### Installation

1. Clone the repo:

```
bash
git clone https://github.com/udacity/cd14600-project-starter.git
cd cd14600-project-starter/starter
```

2. Run the Program: 
```
python main.py
```

## Testing

This project uses Python’s built-in unittest framework.

To run all tests:

```
python -m unittest discover
```

To run a single test file:
```
python -m unittest balance/test_balance_observer.py
```

### Break Down Tests

- test_balance.py → Verifies correct implementation of the Singleton Balance class.
- test_transaction.py → Confirms transactions update balances correctly.
- test_transaction_adapter.py → Ensures external income data is correctly adapted into Transaction objects.
- test_balance_observer.py → Validates that low-balance alerts are triggered at the correct threshold.

## Project Instructions

1. Implement Singleton Balance Class – Ensure only one balance object exists throughout the app.
2. Complete Transaction Class – Handle income and expense transactions.
3. Implement Adapter Pattern – Adapt external freelance income data into internal Transaction objects.
4. Implement Observer Pattern – Create a low balance observer that triggers an alert when funds drop too low.
5. Add Unit Tests – Write tests for all implemented functionality.
6. Choose and Implement a Fourth Pattern – Pick one additional design pattern (e.g., Strategy, Command, Decorator, etc.) and integrate it into your project.
7. Provide a Reflection – Add a short write-up in your repo (README or separate file) explaining your design choices.

## Built With

* [Python](https://www.python.org/) – Main programming language
* [unittest](https://docs.python.org/3/library/unittest.html) – Testing framework
* [PEP8](https://peps.python.org/pep-0008/) – Style guide for Python code

## License

[License](LICENSE.txt)

## Design Pattern Implementation: Strategy Pattern

### Why We Chose the Strategy Pattern

The Strategy pattern was selected to handle different transaction categorization and analysis strategies in the Personal Finance Manager. As users track their finances, they need flexible ways to categorize and analyze their spending patterns—some may prefer category-based analysis, others time-based, and some may want custom rules for tax purposes or budgeting goals.

The Strategy pattern allows us to:
- Define a family of interchangeable algorithms for transaction analysis
- Encapsulate each algorithm independently
- Make algorithms interchangeable at runtime without modifying client code
- Adhere to the Open/Closed Principle (open for extension, closed for modification)

### Where It Fits Into the App

The Strategy pattern is integrated into the transaction analysis module:

**Location:** `analysis/transaction_analyzer.py`

**Components:**
- **Context:** `TransactionAnalyzer` class that uses a strategy to analyze transactions
- **Strategy Interface:** `AnalysisStrategy` abstract base class defining the common interface
- **Concrete Strategies:**
  - `CategoryAnalysisStrategy` – Groups transactions by category (food, rent, entertainment, etc.)
  - `TimeBasedAnalysisStrategy` – Analyzes spending patterns over time periods
  - `BudgetComparisonStrategy` – Compares actual spending against budget limits

**Usage Example:**
```python
# Initialize analyzer with a strategy
analyzer = TransactionAnalyzer(CategoryAnalysisStrategy())
report = analyzer.analyze(transactions)

# Switch strategy at runtime
analyzer.set_strategy(TimeBasedAnalysisStrategy())
monthly_report = analyzer.analyze(transactions)
```

### How It Improves Flexibility, Testability, and Scalability

#### Flexibility
- **Runtime Strategy Switching:** Users can change analysis methods on-the-fly without restarting the application
- **Easy Configuration:** Different user profiles can have different default strategies
- **No Conditional Logic:** Eliminates complex if/else chains for different analysis types

#### Testability
- **Isolated Testing:** Each strategy can be tested independently without dependencies on other strategies
- **Mock Strategies:** Easy to create mock strategies for testing the analyzer context
- **Single Responsibility:** Each strategy has one clear purpose, making unit tests more focused and maintainable

**Example Test:**
```python
def test_category_analysis_strategy():
    strategy = CategoryAnalysisStrategy()
    transactions = [Transaction("Food", 50), Transaction("Food", 30)]
    result = strategy.execute(transactions)
    assert result["Food"] == 80
```

#### Scalability
- **Add New Strategies:** New analysis methods can be added without modifying existing code
- **Plugin Architecture:** Strategies can be loaded dynamically, supporting third-party extensions
- **Parallel Processing:** Different strategies can run concurrently for the same transaction set
- **Reusability:** Strategies can be reused across different parts of the application (reports, dashboards, exports)

**Future Extensions:**
- `TaxOptimizationStrategy` – For tax deduction identification
- `InvestmentAnalysisStrategy` – For analyzing investment transactions
- `SavingsGoalStrategy` – For tracking progress toward savings goals
- `CustomRuleStrategy` – User-defined rules for personalized analysis

### Implementation Benefits Demonstrated

1. **Before Strategy Pattern (Rigid):**
   ```python
   def analyze_transactions(transactions, analysis_type):
       if analysis_type == "category":
           # Category logic here
       elif analysis_type == "time":
           # Time logic here
       elif analysis_type == "budget":
           # Budget logic here
       # Adding new types requires modifying this function
   ```

2. **After Strategy Pattern (Flexible):**
   ```python
   analyzer = TransactionAnalyzer(strategy)
   report = analyzer.analyze(transactions)
   # Adding new strategies requires zero changes to existing code
   ```

This pattern exemplifies good software design by promoting loose coupling, high cohesion, and adherence to SOLID principles, making the Personal Finance Manager more maintainable and extensible
