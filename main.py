# main.py

import os
from storage import load_accounts, save_accounts
from bank import Bank

ADMIN_PASSWORD = os.environ.get("BANK_ADMIN_PASSWORD", "admin123")


# ─────────────────────────── HELPERS ────────────────────────────

def get_float(prompt: str) -> float | None:
    """Prompt for a float. Returns None on invalid input."""
    try:
        value = float(input(prompt).strip())
        return value
    except ValueError:
        print("Invalid amount. Please enter a number.")
        return None


def get_int(prompt: str) -> int | None:
    """Prompt for an int. Returns None on invalid input."""
    try:
        return int(input(prompt).strip())
    except ValueError:
        print("Invalid number.")
        return None


def separator(title: str = ""):
    line = "=" * 40
    if title:
        print(f"\n{line}")
        print(f"  {title}")
        print(line)
    else:
        print(line)


# ─────────────────────────── BANKING MENU ────────────────────────────

def banking_menu(bank: Bank, account):
    while True:
        separator(f"BANK MENU — {account.name} [{account.account_type}]")
        print("1. Check Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Transfer")
        print("5. Show Last Transactions")
        print("6. Change PIN")
        print("7. Logout")

        choice = input("Choose option: ").strip()

        if choice == "1":
            print(f"  Current Balance: ₹{account.balance:,.2f}")

        elif choice == "2":
            amount = get_float("Enter deposit amount: ₹")
            if amount is None:
                continue
            if account.deposit(amount):
                save_accounts(bank.accounts)
                print(f"  ✓ Deposited ₹{amount:,.2f}. New balance: ₹{account.balance:,.2f}")
            else:
                print("  Deposit failed. Amount must be positive and account must be active.")

        elif choice == "3":
            amount = get_float("Enter withdrawal amount: ₹")
            if amount is None:
                continue
            success, message = account.withdraw(amount)
            if success:
                save_accounts(bank.accounts)
                print(f"  ✓ {message} New balance: ₹{account.balance:,.2f}")
            else:
                print(f"  ✗ {message}")

        elif choice == "4":
            recipient_num = input("Enter recipient account number: ").strip()
            amount = get_float("Enter transfer amount: ₹")
            if amount is None:
                continue
            success, message = bank.transfer(account, recipient_num, amount)
            if success:
                print(f"  ✓ {message} New balance: ₹{account.balance:,.2f}")
            else:
                print(f"  ✗ {message}")

        elif choice == "5":
            n = get_int("How many recent transactions to show? ")
            if n is None:
                continue
            transactions = account.get_last_transactions(n)
            if not transactions:
                print("  No transactions found.")
            else:
                print("\n  --- Recent Transactions ---")
                print(f"  {'Date & Time':<22} {'Type':<20} {'Amount':>12}")
                print("  " + "-" * 56)
                for t in transactions:
                    print(f"  {t['time']:<22} {t['type']:<20} ₹{t['amount']:>10,.2f}")

        elif choice == "6":
            old_pin = input("Enter current PIN: ").strip()
            new_pin = input("Enter new 4-digit PIN: ").strip()
            if account.change_pin(old_pin, new_pin):
                save_accounts(bank.accounts)
                print("  ✓ PIN changed successfully.")
            else:
                print("  ✗ PIN change failed. Check your current PIN and ensure new PIN is 4 digits.")

        elif choice == "7":
            print(f"  Logged out. Goodbye, {account.name}!")
            break

        else:
            print("  Invalid option. Please choose 1–7.")


# ─────────────────────────── ADMIN PANEL ────────────────────────────

def admin_panel(bank: Bank):
    admin_password = input("Enter admin password: ").strip()
    if admin_password != ADMIN_PASSWORD:
        print("  Access denied.")
        return

    while True:
        separator("ADMIN PANEL")
        print("1. View All Accounts")
        print("2. Delete Account")
        print("3. Freeze Account")
        print("4. Unfreeze Account")
        print("5. Unlock Account (reset failed attempts)")
        print("6. Bank Statistics")
        print("7. Apply Interest to All Eligible Accounts")
        print("8. Back")

        choice = input("Choose option: ").strip()

        if choice == "1":
            accounts = bank.get_all_accounts()
            if not accounts:
                print("  No accounts found.")
            else:
                print(f"\n  {'Acc#':<8} {'Name':<20} {'Balance':>14} {'Type':<16} {'Status'}")
                print("  " + "-" * 68)
                for acc in accounts:
                    status = "Active" if acc.active else "Frozen"
                    if acc.locked:
                        status = "Locked"
                    print(f"  {acc.account_number:<8} {acc.name:<20} ₹{acc.balance:>12,.2f} "
                          f"{acc.account_type:<16} {status}")

        elif choice == "2":
            acc_num = input("Enter account number to delete: ").strip()
            confirm = input(f"  Are you sure you want to delete account {acc_num}? (yes/no): ").strip().lower()
            if confirm == "yes":
                if bank.delete_account(acc_num):
                    print("  ✓ Account deleted.")
                else:
                    print("  ✗ Account not found.")
            else:
                print("  Deletion cancelled.")

        elif choice == "3":
            acc_num = input("Enter account number to freeze: ").strip()
            if bank.freeze_account(acc_num):
                print("  ✓ Account frozen.")
            else:
                print("  ✗ Account not found.")

        elif choice == "4":
            acc_num = input("Enter account number to unfreeze: ").strip()
            if bank.unfreeze_account(acc_num):
                print("  ✓ Account unfrozen.")
            else:
                print("  ✗ Account not found.")

        elif choice == "5":
            acc_num = input("Enter account number to unlock: ").strip()
            if bank.unlock_account(acc_num):
                print("  ✓ Account unlocked.")
            else:
                print("  ✗ Account not found.")

        elif choice == "6":
            print(f"\n  Total Bank Funds  : ₹{bank.total_bank_funds():,.2f}")
            top = bank.highest_balance_account()
            if top:
                print(f"  Highest Balance   : {top.name} — ₹{top.balance:,.2f}")
            print(f"  Active Users      : {bank.active_users_count()}")

        elif choice == "7":
            bank.apply_interest_all()
            print("  ✓ Interest applied to all eligible accounts.")

        elif choice == "8":
            break

        else:
            print("  Invalid option. Please choose 1–8.")


# ─────────────────────────── MAIN ────────────────────────────

def main():
    accounts = load_accounts()
    bank = Bank(accounts)

    while True:
        separator("BANK SYSTEM")
        print("1. Create Account")
        print("2. Login")
        print("3. Admin Panel")
        print("4. Exit")

        choice = input("Choose option: ").strip()

        if choice == "1":
            name = input("Enter your full name: ").strip()
            pin = input("Set a 4-digit PIN: ").strip()
            deposit = get_float("Initial deposit amount: ₹")
            if deposit is None:
                continue

            print("\nAccount Types:")
            print("  1. Savings     (4% annual interest)")
            print("  2. Current     (no interest)")
            print("  3. Fixed Deposit (6% annual interest, 12-month lock)")
            atype = input("Choose type (1/2/3): ").strip()
            types = {"1": "Savings", "2": "Current", "3": "Fixed Deposit"}
            account_type = types.get(atype, "Savings")

            account, message = bank.create_account(name, pin, deposit, account_type)
            print(f"\n  {message}")
            if account:
                print(f"  Your account number is: {account.account_number}")
                if account.fd_maturity:
                    print(f"  FD Maturity Date: {account.fd_maturity}")

        elif choice == "2":
            acc_num = input("Enter account number: ").strip()
            pin = input("Enter PIN: ").strip()

            account = bank.login(acc_num, pin)
            if account:
                print(f"\n  Welcome back, {account.name}!")
                banking_menu(bank, account)
            else:
                print("  Login failed. Check your account number and PIN.")

        elif choice == "3":
            admin_panel(bank)

        elif choice == "4":
            print("\n  Thank you for banking with us. Goodbye!")
            break

        else:
            print("  Invalid choice. Please select 1–4.")


if __name__ == "__main__":
    main()
