import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QCheckBox, QHBoxLayout, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login Panel")
        self.setFixedSize(350, 400)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(40, 30, 40, 30)

        # Title
        title = QLabel("🔒 Welcome Back!")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("Please login to continue")
        subtitle.setAlignment(Qt.AlignCenter)

        # Username
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")

        # Password
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)

        # Show password checkbox
        self.show_password_checkbox = QCheckBox("Show Password")
        self.show_password_checkbox.stateChanged.connect(self.toggle_password_visibility)

        # Login button
        login_button = QPushButton("LOGIN")
        login_button.clicked.connect(self.login)

        # Forgot password link (dummy label)
        forgot_label = QLabel("<a href='#'>Forgot password?</a>")
        forgot_label.setAlignment(Qt.AlignCenter)
        forgot_label.setOpenExternalLinks(True)

        # Register label
        register_label = QLabel("Don’t have an account? <a href='#'>Register</a>")
        register_label.setAlignment(Qt.AlignCenter)
        register_label.setOpenExternalLinks(True)

        # Add widgets to layout
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.show_password_checkbox)
        layout.addWidget(login_button)
        layout.addWidget(forgot_label)
        layout.addWidget(register_label)

        self.setLayout(layout)

    def toggle_password_visibility(self, state):
        if state == Qt.Checked:
            self.password_input.setEchoMode(QLineEdit.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.Password)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        # Dummy check (replace with real auth logic)
        if username == "admin" and password == "1234":
            QMessageBox.information(self, "Success", "Login successful!")
        else:
            QMessageBox.warning(self, "Error", "Invalid username or password.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
