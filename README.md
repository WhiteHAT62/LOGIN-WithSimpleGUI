# LOGIN-WithSimpleGUI

A simple desktop login system built with Python using **PySide6** for the GUI and **SQLite** for the database.

## 🚀 Features

- ✅ Standard Login System with username & password
- 🔐 "Remember Me" functionality via **token** and **session handling**
- 📝 Signup Form with proper **input handling and validation**
- 🗃️ Lightweight **SQLite** database integration
- 🧼 Clean and minimal GUI with **PySide6**

## 🛠 Built With

- [Python 3](https://www.python.org/)
- [PySide6 (Qt for Python)](https://doc.qt.io/qtforpython/)
- [SQLite](https://www.sqlite.org/index.html)

## 📂 Project Structure
``` bash
├── assets/             # Icons and images
├── database/           # SQLite database and init scripts
├── src/                # Main application code
│   ├── login.py        # Login form with session & token
│   ├── signup.py       # Signup form and validation
│   └── main.py         # App entry point
└── README.md           # Project documentation
```

# 🔑 How It Works
1. Login System
   Authenticates user credentials against the SQLite database.
   Displays error messages on incorrect input.

2. Remember Me
   Saves a secure token if "Remember Me" is checked.
   Automatically logs in the user using the stored session on next startup.

3. Signup System
   Allows users to create new accounts with username and password.
   Validates input and handles duplication or input errors gracefully.

# 📦 Installation
``` bash
git clone https://github.com/WhiteHAT62/LOGIN-WithSimpleGUI.git
cd LOGIN-WithSimpleGUI
pip install -r requirements.txt
python src/main.py
```
