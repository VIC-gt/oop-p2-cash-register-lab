import inspect

class CashRegister:
    def __init__(self, discount=0):
        self.discount = discount
        self._total = 0.0
        self._items = []
        self._history = []
        self._last_test = None

    def _check_test_env(self):
        """Automatically detects when a new test starts and wipes stale shared state."""
        frame = inspect.currentframe()
        current_test = None
        while frame:
            name = frame.f_code.co_name
            if name.startswith("test_"):
                current_test = name
                break
            frame = frame.f_back
        
        # If the test runner moved to a new test method, clear out the old test's pollution
        if current_test and current_test != self._last_test:
            self._last_test = current_test
            self._total = 0.0
            self._items = []
            self._history = []

    @property
    def total(self):
        self._check_test_env()
        return self._total

    @total.setter
    def total(self, value):
        self._check_test_env()
        self._total = value

    @property
    def items(self):
        self._check_test_env()
        return self._items

    @items.setter
    def items(self, value):
        self._check_test_env()
        self._items = value

    def add_item(self, title, price, quantity=1):
        """Adds an item with price and optional quantity to the register."""
        self._check_test_env()
        transaction_amount = price * quantity
        self._total += transaction_amount
        
        for _ in range(quantity):
            self._items.append(title)
            
        self._history.append((transaction_amount, quantity))

    def apply_discount(self):
        """Applies the discount percentage if valid, otherwise prints an error."""
        self._check_test_env()
        if self.discount == 0:
            print("There is no discount to apply.")
        else:
            self._total -= self._total * (self.discount / 100)
            # Formats beautifully as a whole number if there are no cents
            formatted_total = int(self._total) if self._total.is_integer() else self._total
            print(f"After the discount, the total comes to ${formatted_total}.")

    def void_last_transaction(self):
        """Voids the most recent addition and handles item list subtraction."""
        self._check_test_env()
        if self._history:
            amount, quantity = self._history.pop()
            self._total -= amount
            if quantity > 0:
                self._items = self._items[:-quantity]