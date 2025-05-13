import sys
import os
import re
import sqlite3
import bcrypt
from PySide6.QtWidgets import QLineEdit, QMessageBox, QGraphicsDropShadowEffect
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QLabel, QHBoxLayout, QVBoxLayout,
    QPushButton, QSizePolicy, QFrame
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QCursor, QPixmap, QColor, QIcon


def hash_data(what_data):
    return bcrypt.hashpw(what_data.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_data(what_data, hashed):
    return bcrypt.checkpw(what_data.encode('utf-8'), hashed)

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class TitleBarLogin(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setFixedSize(500, 40)
        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("background-color: #2A2A40;")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        icon = QLabel()
        icon_pixmap = QPixmap(resource_path("assets/ikon.ico")).scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        icon.setPixmap(icon_pixmap)
        icon.setStyleSheet("padding-left: 10px")
        layout.addWidget(icon)

        text = QLabel("PASSWORD MANAGER")
        text.setStyleSheet("color: white; font-weight: bold; padding-left: 1px")
        layout.addWidget(text)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(spacer)

        frame_min = QFrame()
        frame_min.setFrameShape(QFrame.NoFrame)
        frame_min.setStyleSheet("background-color: #2A2A40;")

        layout_min_frame = QVBoxLayout()
        layout_min_frame.setContentsMargins(0, 0, 0, 0)
        layout_min_frame.setAlignment(Qt.AlignmentFlag.AlignCenter)

        tombol_min = QPushButton("⛔️")
        tombol_min.setFixedSize(30, 30)
        tombol_min.setFont(QFont("Arial", 14))
        tombol_min.setStyleSheet("""
                    QPushButton {
                        color: white;
                        border: none;
                    }
                    QPushButton:hover {
                        background-color: #44475a;
                    }
                """)
        tombol_min.clicked.connect(self.parent.showMinimized)
        layout_min_frame.addWidget(tombol_min)
        frame_min.setLayout(layout_min_frame)
        layout.addWidget(frame_min)

        frame_ex = QFrame()
        frame_ex.setFrameShape(QFrame.NoFrame)
        frame_ex.setStyleSheet("background-color: #2A2A40;")

        layout_ex_frame = QHBoxLayout()
        layout_ex_frame.setContentsMargins(0, 0, 5, 0)
        layout_ex_frame.setAlignment(Qt.AlignmentFlag.AlignCenter)

        tombol_ex = QPushButton("❌")
        tombol_ex.setFixedSize(30, 30)
        tombol_ex.setFont(QFont("Arial", 14))
        tombol_ex.setStyleSheet("""
                    QPushButton {
                        color: white;
                        border: none;
                    }
                    QPushButton:hover {
                        background-color: #44475a;
                    }
                """)
        tombol_ex.clicked.connect(self.parent.close)
        layout_ex_frame.addWidget(tombol_ex)
        frame_ex.setLayout(layout_ex_frame)
        layout.addWidget(frame_ex)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_start_position = event.globalPosition().toPoint()
            if hasattr(self.parent, 'windowHandle') and self.parent.windowHandle():
                self.parent.windowHandle().startSystemMove()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            if hasattr(self, 'drag_start_position'):
                delta = event.globalPosition().toPoint() - self.drag_start_position
                self.parent.move(self.parent.pos() + delta)
                self.drag_start_position = event.globalPosition().toPoint()
                event.accept()

class LoginWindow(QMainWindow):
    def __init__(self, on_login_success=None):
        super().__init__()
        self.on_login_success = on_login_success
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Window)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(500, 340)

        self.container = QWidget()
        self.container.setStyleSheet("background: #1E1E2C")
        self.setCentralWidget(self.container)

        layout = QVBoxLayout(self.container)
        layout.setContentsMargins(0, 0, 0, 0)

        self.title_bar = TitleBarLogin(self)
        layout.addWidget(self.title_bar)

        self.content = QWidget()
        content_layout = QVBoxLayout(self.content)
        content_layout.setContentsMargins(50, 0, 50, 0)

        welcome = QLabel("🔐 WELCOME BACK!")
        welcome.setFont(QFont("Arial", 16, QFont.Bold))
        welcome.setStyleSheet("margin-top: 15px")
        welcome.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(welcome)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("🆔 Username")
        self.username_input.setFont(QFont("Segoe UI", 12))
        self.username_input.setStyleSheet("""
            QLineEdit {
                background: #2A2A40;
                color: white;
                padding: 8px;
                margin-top: 15px;
                border-radius: 8px;
                border: 1px solid #444;
            }
            QLineEdit:focus {
                border: 1px solid #00FFA3;
            }
        """)
        self.username_input.returnPressed.connect(self.handle_login)
        content_layout.addWidget(self.username_input)

        password_layout = QHBoxLayout()
        password_layout.setContentsMargins(0, 0, 0, 0)
        password_layout.setSpacing(5)

        # Password input
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("🔒 Password")
        self.password_input.setFont(QFont("Segoe UI", 12))
        self.password_input.setStyleSheet("""
            QLineEdit {
                background: #2A2A40;
                color: white;
                padding: 8px;
                border-radius: 8px;
                border: 1px solid #444;
            }
            QLineEdit:focus {
                border: 1px solid #00FFA3;
            }
        """)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.returnPressed.connect(self.handle_login)

        # Eye toggle button
        self.toggle_password_button = QPushButton("👁️")
        self.toggle_password_button.setCheckable(True)
        self.toggle_password_button.setFixedSize(39, 39)
        self.toggle_password_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.toggle_password_button.setFont(QFont("Segoe UI", 15))
        self.toggle_password_button.setStyleSheet("""
            QPushButton {
                background: #2A2A40;
                color: white;
                border-radius: 8px;
                border: 1px solid #444;
            }
            QPushButton:pressed {
                background-color: #444;
            }
        """)

        self.toggle_password_button.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.toggle_password_button.clicked.connect(self.toggle_password_visibility)

        password_layout.addWidget(self.password_input)
        password_layout.addWidget(self.toggle_password_button)
        content_layout.addLayout(password_layout)

        from PySide6.QtWidgets import QCheckBox
        self.remember_me_checkbox = QCheckBox("Remember me")
        self.remember_me_checkbox.setStyleSheet("color: #B0B0C3;")
        content_layout.addWidget(self.remember_me_checkbox)

        login_button = QPushButton("Login")
        login_button.setFont(QFont("Arial", 12, QFont.Bold))
        login_button.setStyleSheet("""
                    QPushButton {
                        color: white;
                        background-color: #00FFA3;
                        padding: 10px;
                    }
                    QPushButton:hover {
                        background-color: #00CC84;
                    }
                """)
        login_button.clicked.connect(self.handle_login)
        content_layout.addWidget(login_button)

        signup_label = QLabel('<a href="#">Belum memiliki akun? Daftar di sini</a>')
        signup_label.setFont(QFont("Arial", 10))
        signup_label.setAlignment(Qt.AlignCenter)
        signup_label.setStyleSheet("color: #00D9FF;")
        signup_label.setOpenExternalLinks(False)
        signup_label.setCursor(QCursor(Qt.PointingHandCursor))
        signup_label.linkActivated.connect(self.handle_signup)
        content_layout.addWidget(signup_label)

        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: red; font-size: 12px;")
        content_layout.addWidget(self.status_label)

        layout.addWidget(self.content)

    def verify_data(what_data, hashed):
        return bcrypt.checkpw(what_data.encode('utf-8'), hashed)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        conn = sqlite3.connect("main.db")
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()

            if not user:
                self.status_label.setText("Username tidak ditemukan.")
                return

            hashed_password = user[0]

            if verify_data(password, hashed_password.encode('utf-8')):

                from Main import save_remember_me_token, clear_remember_me_token
                if self.remember_me_checkbox.isChecked():
                    save_remember_me_token(username)
                else:
                    clear_remember_me_token()

                if self.on_login_success:
                    self.close()
                    self.on_login_success(username)
            else:
                self.status_label.setText("Incorrect password. Try again.")
        except sqlite3.Error as e:
            self.status_label.setText(f"Database error: {e}")
        finally:
            conn.close()

    def handle_signup(self):
        self.close()
        self.daftar_window = DaftarWindow()
        self.daftar_window.show()

    def toggle_password_visibility(self):
        if self.toggle_password_button.isChecked():
            self.password_input.setEchoMode(QLineEdit.Normal)
            self.toggle_password_button.setText("🙈")
        else:
            self.password_input.setEchoMode(QLineEdit.Password)
            self.toggle_password_button.setText("👁️")

class DaftarWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Window)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(500, 500)

        self.container = QWidget()
        self.container.setStyleSheet("""
            QWidget#container_bg {
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1,
                stop:0 #1E1E2C, stop:1 #2A2A40);
                border-radius: 15px;
            }
        """)
        self.container.setObjectName("container_bg")
        self.setCentralWidget(self.container)

        wrapper_layout = QVBoxLayout(self.container)
        wrapper_layout.setContentsMargins(0, 0, 0, 0)
        wrapper_layout.setSpacing(0)

        # Title bar
        self.title_bar = TitleBarLogin(self)
        wrapper_layout.addWidget(self.title_bar)

        # Content area
        self.content = QWidget()
        self.content.setObjectName("content_area")
        self.content.setStyleSheet("""
            QWidget#content_area {
                background: transparent;
                border-top-left-radius: 0;
                border-top-right-radius: 0;
                border-bottom-left-radius: 15px;
                border-bottom-right-radius: 15px;
            }
        """)

        content_layout = QVBoxLayout(self.content)
        content_layout.setContentsMargins(50, 0, 50, 0)

        welcome = QLabel("📝 CREATE YOUR ACCOUNT")
        welcome.setFont(QFont("Segoe UI", 18, QFont.Bold))
        welcome.setStyleSheet("margin-top: 10px; color: white;")
        welcome.setAlignment(Qt.AlignmentFlag.AlignCenter)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(2)
        shadow.setColor(QColor(0, 255, 163))
        welcome.setGraphicsEffect(shadow)
        welcome.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(welcome)

        def styled_input(placeholder):
            inp = QLineEdit()
            inp.setPlaceholderText(f"  {placeholder}")
            inp.setFont(QFont("Segoe UI", 12))
            inp.setStyleSheet("""
                QLineEdit {
                    background: #2A2A40;
                    color: white;
                    padding: 8px;
                    margin-top: 10px;
                    border-radius: 8px;
                    border: 1px solid #444;
                }
                QLineEdit:focus {
                    border: 1px solid #00FFA3;
                }
            """)
            return inp

        self.name_input = styled_input("👤 Your Name")
        self.username_input = styled_input("🆔 Username")
        self.email_input = styled_input("📧 Email")
        self.password_input = styled_input("🔒 Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_password_input = styled_input("🔒✅ Confirm Password")
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)

        for field in [self.name_input, self.username_input, self.email_input,
                      self.password_input, self.confirm_password_input]:
            content_layout.addWidget(field)

        register_button = QPushButton("Register")
        register_button.setFont(QFont("Segoe UI", 12, QFont.Bold))
        register_button.setCursor(Qt.PointingHandCursor)
        register_button.setStyleSheet("""
            QPushButton {
                color: black;
                background-color: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #00FFA3, stop:1 #00CC84);
                padding: 10px;
                margin-top: 20px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #00CC84;
            }
        """)
        register_button.clicked.connect(self.handle_register)
        content_layout.addWidget(register_button)

        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: red; font-size: 12px; margin-top: 5px;")
        content_layout.addWidget(self.status_label)

        wrapper_layout.addWidget(self.content)

    def handle_register(self):
        name = self.name_input.text()
        username = self.username_input.text()
        email = self.email_input.text()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()

        if not name or not username or not email or not password or not confirm_password:
            self.status_label.setText("All fields are required.")
            return

        if len(name) > 27 or not re.fullmatch(r"[A-Za-z\s]+", name):
            self.status_label.setText("Name must only contain letters and spaces (max 27 chars).")
            return

        if len(username) > 15 or not re.fullmatch(r"[A-Za-z0-9_@]+", username):
            self.status_label.setText("Username can only contain letters, numbers, @, and _ (no spaces, max 15 chars).")
            return

        from email_validator import validate_email, EmailNotValidError
        if len(email) > 25:
            self.status_label.setText("Email must be under 25 characters.")
            return

        try:
            valid = validate_email(email)
            email = valid.email
        except EmailNotValidError as e:
            self.status_label.setText(f"Invalid email: {e}")
            return

        if len(password) < 6 or len(password) > 12:
            self.status_label.setText("Password must be 6–12 characters long.")
            return
        if not re.search(r"[A-Za-z]", password) or not re.search(r"[0-9]", password) or not re.search(r"[^\w\s]",
                                                                                                      password):
            self.status_label.setText("Password must contain letters, numbers, and at least one special character.")
            return

        if password != confirm_password:
            self.status_label.setText("Passwords do not match.")
            return

        h_email = hash_data(email)
        h_password = hash_data(password)

        try:
            conn = sqlite3.connect("main.db")
            cursor = conn.cursor()

            cursor.execute("""
                           INSERT INTO users (name, username, email, password)
                           VALUES (?, ?, ?, ?)""",
                           (name, username, h_email, h_password)
                           )

            table_name = f"user_{username}"
            table_name = ''.join(c for c in table_name if c.isalnum() or c == '_')

            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    data TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            conn.commit()
            conn.close()

            QMessageBox.information(self, "Success", "Account created successfully!")
            self.close()
            from Main import App
            self.app = App().run()

        except sqlite3.IntegrityError:
            self.status_label.setText("Username or email already exists.")
        except sqlite3.Error as e:
            self.status_label.setText(f"Database error: {e}")
