from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from datetime import datetime, timedelta

from LoginPanel import LoginWindow
from halamanutama import HalamanUtama
from splashscreen import SplashScreen

import os
import sys
import sqlite3
import secrets

import json

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def initialize_database():
    database_name = "main.db"

    if not os.path.exists(database_name):
        print(f"Membuat database '{database_name}'...")
        conn = sqlite3.connect(database_name)
        conn.close()
    else:
        print(f"Database '{database_name}' sudah ada.")

    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        );
    """)
    print("Tabel 'users' siap.")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS token (
            user_id INTEGER NOT NULL,
            remember_token TEXT,
            token_expiry TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        );
    """)
    print("Tabel 'token' siap.")

    conn.commit()
    conn.close()

def get_remember_me_token():
    if not os.path.exists("remember_me.json"):
        return None

    with open("remember_me.json", "r") as file:
        data = json.load(file)
        token = data.get("token")

    if not token:
        return None

    conn = sqlite3.connect("main.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT users.username, token.token_expiry
        FROM token
        JOIN users ON users.id = token.user_id
        WHERE token.remember_token = ?
    """, (token,))
    result = cursor.fetchone()
    conn.close()

    if result:
        username, expiry_str = result
        if datetime.now() < datetime.fromisoformat(expiry_str):
            return username
        else:
            clear_remember_me_token()

    return None

def save_remember_me_token(username):
    token = secrets.token_urlsafe(32)
    expiry_time = datetime.now() + timedelta(hours=3)

    conn = sqlite3.connect("main.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    if not user:
        conn.close()
        return

    user_id = user[0]
    cursor.execute("DELETE FROM token WHERE user_id = ?", (user_id,))

    cursor.execute("""
        INSERT INTO token (user_id, remember_token, token_expiry)
        VALUES (?, ?, ?)
    """, (user_id, token, expiry_time.isoformat()))
    conn.commit()
    conn.close()

    with open("remember_me.json", "w") as file:
        json.dump({"token": token}, file)

def clear_remember_me_token():
    if not os.path.exists("remember_me.json"):
        return

    with open("remember_me.json", "r") as file:
        data = json.load(file)
        token = data.get("token")

    if token:
        conn = sqlite3.connect("main.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM token WHERE remember_token = ?", (token,))
        conn.commit()
        conn.close()

    os.remove("remember_me.json")

class App:
    def __init__(self):
        self.remembered_user = get_remember_me_token()
        self.logged_in_user_id = None
        if self.remembered_user:
            self.show_main_window(self.remembered_user)
        else:
            self.show_login_window()

    def show_login_window(self):
        self.login_window = LoginWindow(on_login_success=lambda username: self.show_main_window(username))
        self.login_window.show()

    def show_main_window(self, username):
        conn = sqlite3.connect("main.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()

        if user:
            self.logged_in_user_id = user[0]
            self.main_window = HalamanUtama(self.logged_in_user_id)
            self.main_window.logout_signal.connect(self.show_login_window)
            self.main_window.show()
            if hasattr(self, 'login_window'):
                self.login_window.close()

    def run(self):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(resource_path("assets/ikon_saya.png")))

    splash = SplashScreen()
    splash.show_splash()
    initialize_database()

    def initialize_app():
        global my_app
        splash.close()
        my_app = App()

    QTimer.singleShot(3000, initialize_app)
    sys.exit(app.exec())

