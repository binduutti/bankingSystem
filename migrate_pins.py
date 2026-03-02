# migrate_pins.py
# Run this ONCE to migrate accounts.json from plaintext PINs to hashed PINs.
# Usage: python migrate_pins.py

import json
import os
import hashlib

FILE_NAME = "accounts.json"


def hash_pin(pin: str) -> str:
    return hashlib.sha256(pin.encode()).hexdigest()


def is_already_hashed(pin: str) -> bool:
    """SHA-256 hashes are 64 hex characters."""
    return len(pin) == 64 and all(c in "0123456789abcdef" for c in pin)


def migrate():
    if not os.path.exists(FILE_NAME):
        print("No accounts.json found. Nothing to migrate.")
        return

    with open(FILE_NAME, "r") as f:
        data = json.load(f)

    migrated = 0
    for acc in data:
        pin = acc.get("pin", "")
        if not is_already_hashed(pin):
            acc["pin"] = hash_pin(pin)
            migrated += 1

    tmp = FILE_NAME + ".tmp"
    with open(tmp, "w") as f:
        json.dump(data, f, indent=4)
    os.replace(tmp, FILE_NAME)

    print(f"Migration complete. {migrated} account(s) updated.")


if __name__ == "__main__":
    migrate()
