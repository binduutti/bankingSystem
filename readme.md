# Python CLI Banking System

A simple **terminal-based banking application** built with Python.
This project demonstrates **object-oriented programming, file-based persistence, and secure PIN handling** using only the Python standard library.

The system supports creating accounts, managing funds, transfers, and an admin panel — all running in the command line.

---

# Features

### User Features

- Create **Savings, Current, or Fixed Deposit** accounts
- Secure **4-digit PIN authentication** using SHA-256 hashing
- Deposit and withdraw funds
- Transfer money between accounts
- View recent transaction history
- Change account PIN
- Automatic **account lock after 3 failed login attempts**

### Admin Features

- View all accounts with status _(Active / Frozen / Locked)_
- Freeze, unfreeze, unlock, or delete accounts
- Apply interest to eligible accounts
- View bank statistics:

  - Total funds
  - Highest balance
  - Active user count

---

# Tech Stack

- **Python 3.10+**
- Python Standard Library only:

  - `hashlib`
  - `json`
  - `os`
  - `random`
  - `datetime`

No external dependencies required.

---

# Project Structure

```
.
├── main.py           # CLI interface and menus
├── bank.py           # Bank logic and account management
├── account.py        # Account operations and PIN security
├── storage.py        # File persistence using JSON
├── migrate_pins.py   # Script to hash existing plaintext PINs
└── accounts.json     # Auto-generated account storage
```

---

# Setup

Make sure Python **3.10 or newer** is installed.

Clone the repository and run the program:

```
git clone https://github.com/yourname/banking-system.git
cd banking-system
python main.py
```

The file **`accounts.json`** will be created automatically when the first account is added.

---

# Running the Application

Start the program:

```
python main.py
```

Main menu example:

```
========================================
  BANK SYSTEM
========================================
1. Create Account
2. Login
3. Admin Panel
4. Exit
```

Default admin password:

```
admin123
```

You can override it using an environment variable:

```
BANK_ADMIN_PASSWORD=mysecretpassword python main.py
```

---

# Data Migration (Optional)

If you have older data with plaintext PINs, run the migration script once:

```
python migrate_pins.py
```

This converts existing PINs to **SHA-256 hashed values**.

---

# Possible Improvements

- Add **SQLite database support**
- Implement **unit tests**
- Add **audit logs for admin actions**
- Support **CLI arguments for automation**
- Implement **session handling**

---

# Contributing

Contributions are welcome.
Please keep the project structure consistent:

- **Account logic → `account.py`**
- **Bank-level operations → `bank.py`**
- **CLI interface → `main.py`**
- **Data persistence → `storage.py`**

Always use `save_accounts()` in `storage.py` to maintain **atomic file writes**.

---

# License

This project is open source and available for learning and experimentation.
