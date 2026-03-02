# storage.py

import json
import os
from account import Account

FILE_NAME = "accounts.json"


def load_accounts() -> list[Account]:
    """Load accounts from JSON. Returns empty list if file missing or malformed."""
    if not os.path.exists(FILE_NAME):
        return []

    try:
        with open(FILE_NAME, "r") as f:
            data = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"[Warning] Could not load accounts file: {e}. Starting fresh.")
        return []

    accounts = []
    for acc in data:
        try:
            accounts.append(Account(
                acc["account_number"],
                acc["name"],
                acc["pin"],
                acc.get("balance", 0),
                acc.get("account_type", "Savings"),
                acc.get("transactions", []),
                acc.get("failed_attempts", 0),
                acc.get("locked", False),
                acc.get("active", True),
                acc.get("fd_maturity", None)
            ))
        except KeyError as e:
            print(f"[Warning] Skipping malformed account record (missing field: {e}).")

    return accounts


def save_accounts(accounts: list[Account]):
    """Persist accounts to JSON file atomically."""
    tmp_file = FILE_NAME + ".tmp"
    try:
        with open(tmp_file, "w") as f:
            json.dump([acc.to_dict() for acc in accounts], f, indent=4)
        os.replace(tmp_file, FILE_NAME)  # Atomic replace prevents corruption
    except IOError as e:
        print(f"[Error] Could not save accounts: {e}")
