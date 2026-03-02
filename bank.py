# bank.py

import random
from account import Account, hash_pin
from storage import save_accounts


class Bank:
    def __init__(self, accounts: list[Account]):
        self.accounts = accounts

    # ---------------- ACCOUNT SEARCH ----------------

    def find_account(self, account_number: str) -> Account | None:
        for acc in self.accounts:
            if acc.account_number == account_number:
                return acc
        return None

    # ---------------- GENERATE ACCOUNT NUMBER ----------------

    def generate_account_number(self) -> str:
        existing = {acc.account_number for acc in self.accounts}
        while True:
            acc_num = str(random.randint(1000, 9999))
            if acc_num not in existing:
                return acc_num

    # ---------------- CHECK USERNAME EXISTS ----------------

    def username_exists(self, name: str) -> bool:
        """BUG FIX: Previously returned inside loop, only checking the first account."""
        return any(acc.name.lower() == name.lower() for acc in self.accounts)

    # ---------------- CREATE ACCOUNT ----------------

    def create_account(self, name: str, pin: str, deposit: float,
                       account_type: str = "Savings") -> tuple[Account | None, str]:
        if not name.strip():
            return None, "Name cannot be empty."
        if self.username_exists(name):
            return None, "Username already exists. Please try a different name."
        if not pin.isdigit() or len(pin) != 4:
            return None, "PIN must be exactly 4 digits."
        if deposit < 0:
            return None, "Initial deposit cannot be negative."

        acc_num = self.generate_account_number()
        account = Account(acc_num, name, hash_pin(pin), deposit, account_type)

        if account_type == "Fixed Deposit":
            account.setup_fixed_deposit(months=12)

        self.accounts.append(account)
        save_accounts(self.accounts)
        return account, "Account created successfully."

    # ---------------- LOGIN ----------------

    def login(self, account_number: str, pin: str) -> Account | None:
        account = self.find_account(account_number)
        if not account:
            return None
        if not account.active:
            print("Account is frozen.")
            return None
        if account.locked:
            print("Account is locked due to multiple failed attempts. Please contact admin.")
            return None
        if account.check_pin(pin):
            save_accounts(self.accounts)
            return account

        remaining = max(0, 3 - account.failed_attempts)
        if account.locked:
            print("Account locked after too many failed attempts.")
        else:
            print(f"Incorrect PIN. {remaining} attempt(s) remaining.")
        save_accounts(self.accounts)
        return None

    # ---------------- TRANSFER ----------------

    def transfer(self, sender: Account, recipient_number: str,
                 amount: float) -> tuple[bool, str]:
        if sender.account_number == recipient_number:
            return False, "Cannot transfer to your own account."

        recipient = self.find_account(recipient_number)
        if not recipient:
            return False, "Recipient account not found."

        success, message = sender.transfer(recipient, amount)
        if success:
            save_accounts(self.accounts)
        return success, message

    # ---------------- APPLY INTEREST ----------------

    def apply_interest_all(self):
        """Apply interest to Savings and Fixed Deposit accounts only."""
        for acc in self.accounts:
            acc.apply_interest()
        save_accounts(self.accounts)

    # ---------------- ADMIN FUNCTIONS ----------------

    def get_all_accounts(self) -> list[Account]:
        return self.accounts

    def delete_account(self, account_number: str) -> bool:
        acc = self.find_account(account_number)
        if acc:
            self.accounts.remove(acc)
            save_accounts(self.accounts)
            return True
        return False

    def freeze_account(self, account_number: str) -> bool:
        acc = self.find_account(account_number)
        if acc:
            acc.active = False
            save_accounts(self.accounts)
            return True
        return False

    def unfreeze_account(self, account_number: str) -> bool:
        acc = self.find_account(account_number)
        if acc:
            acc.active = True
            save_accounts(self.accounts)
            return True
        return False

    def unlock_account(self, account_number: str) -> bool:
        acc = self.find_account(account_number)
        if acc:
            acc.locked = False
            acc.failed_attempts = 0
            save_accounts(self.accounts)
            return True
        return False

    # ---------------- REPORTS & STATISTICS ----------------

    def total_bank_funds(self) -> float:
        return round(sum(acc.balance for acc in self.accounts), 2)

    def highest_balance_account(self) -> Account | None:
        if not self.accounts:
            return None
        return max(self.accounts, key=lambda x: x.balance)

    def active_users_count(self) -> int:
        return sum(1 for acc in self.accounts if acc.active)
