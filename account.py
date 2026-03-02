# account.py

import hashlib
from datetime import datetime, timedelta


def hash_pin(pin: str) -> str:
    """SHA-256 hash a PIN string."""
    return hashlib.sha256(pin.encode()).hexdigest()


class Account:
    def __init__(self, account_number, name, pin, balance=0,
                 account_type="Savings",
                 transactions=None,
                 failed_attempts=0,
                 locked=False,
                 active=True,
                 fd_maturity=None):

        self.account_number = account_number
        self.name = name
        self.pin = pin  # Expected to be stored as a hash
        self.balance = float(balance)
        self.account_type = account_type
        self.transactions = transactions if transactions is not None else []
        self.failed_attempts = int(failed_attempts)
        self.locked = locked
        self.active = active
        self.fd_maturity = fd_maturity  # Used only for Fixed Deposit

    # ---------------- PIN HANDLING ----------------

    def check_pin(self, pin: str) -> bool:
        """Verify PIN against stored hash. Locks account after 3 failures."""
        if not self.active:
            return False
        if self.locked:
            return False

        if self.pin == hash_pin(pin):
            self.failed_attempts = 0
            return True

        self.failed_attempts += 1
        if self.failed_attempts >= 3:
            self.locked = True
        return False

    def change_pin(self, old_pin: str, new_pin: str) -> bool:
        """Change PIN if old PIN matches. Validates 4-digit format."""
        if not new_pin.isdigit() or len(new_pin) != 4:
            return False
        if self.pin == hash_pin(old_pin):
            self.pin = hash_pin(new_pin)
            return True
        return False

    # ---------------- TRANSACTION HANDLING ----------------

    def add_transaction(self, type_: str, amount: float):
        self.transactions.append({
            "type": type_,
            "amount": round(float(amount), 2),
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    def get_last_transactions(self, n: int = 5) -> list:
        return self.transactions[-n:]

    # ---------------- DEPOSIT ----------------

    def deposit(self, amount: float) -> bool:
        if not self.active:
            return False
        if amount <= 0:
            return False
        self.balance += round(amount, 2)
        self.add_transaction("Deposit", amount)
        return True

    # ---------------- WITHDRAW ----------------

    def withdraw(self, amount: float) -> tuple[bool, str]:
        """
        Returns (success: bool, message: str).
        """
        if not self.active:
            return False, "Account is not active."
        if amount <= 0:
            return False, "Withdrawal amount must be positive."

        # Fixed Deposit restriction
        if self.account_type == "Fixed Deposit" and self.fd_maturity:
            maturity_date = datetime.strptime(self.fd_maturity, "%Y-%m-%d")
            if datetime.now() < maturity_date:
                return False, f"Fixed Deposit matures on {self.fd_maturity}. Early withdrawal is not allowed."

        if amount > self.balance:
            return False, "Insufficient balance."

        self.balance -= round(amount, 2)
        self.add_transaction("Withdraw", amount)
        return True, "Withdrawal successful."

    # ---------------- TRANSFER ----------------

    def transfer(self, recipient: "Account", amount: float) -> tuple[bool, str]:
        """
        Returns (success: bool, message: str).
        """
        if not self.active:
            return False, "Your account is not active."
        if not recipient.active:
            return False, "Recipient account is not active."
        if amount <= 0:
            return False, "Transfer amount must be positive."
        if amount > self.balance:
            return False, "Insufficient balance."

        self.balance -= round(amount, 2)
        recipient.balance += round(amount, 2)
        self.add_transaction("Transfer Sent", amount)
        recipient.add_transaction("Transfer Received", amount)
        return True, "Transfer successful."

    # ---------------- INTEREST ----------------

    def apply_interest(self) -> float:
        """Apply interest based on account type. Returns interest amount."""
        if not self.active:
            return 0.0

        rates = {"Savings": 0.04, "Fixed Deposit": 0.06}
        rate = rates.get(self.account_type)
        if rate is None:
            return 0.0  # Current accounts earn no interest

        interest = round(self.balance * rate, 2)
        self.balance += interest
        label = "FD Interest" if self.account_type == "Fixed Deposit" else "Interest"
        self.add_transaction(label, interest)
        return interest

    # ---------------- FIXED DEPOSIT SETUP ----------------

    def setup_fixed_deposit(self, months: int = 12):
        if self.account_type == "Fixed Deposit":
            maturity_date = datetime.now() + timedelta(days=30 * months)
            self.fd_maturity = maturity_date.strftime("%Y-%m-%d")

    # ---------------- CONVERT TO DICTIONARY ----------------

    def to_dict(self) -> dict:
        return {
            "account_number": self.account_number,
            "name": self.name,
            "pin": self.pin,
            "balance": round(self.balance, 2),
            "account_type": self.account_type,
            "transactions": self.transactions,
            "failed_attempts": self.failed_attempts,
            "locked": self.locked,
            "active": self.active,
            "fd_maturity": self.fd_maturity
        }
