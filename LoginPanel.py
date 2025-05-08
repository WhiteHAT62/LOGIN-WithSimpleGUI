import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit,
    QPushButton, QLabel, QCheckBox, QMessageBox,
    QHBoxLayout, QMainWindow
)
from PySide6.QtGui import QFont, QCursor, QIcon
from PySide6.QtCore import Qt


class LoginForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PASSWORD MANAGER")
        self.setFixedSize(400, 340)
        self.setup_ui()

    def setup_ui(self):
        # Main layout
        layout = QVBoxLayout(self)

        # Title Label
        title_label = QLabel("Welcome Back!")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Username Input
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setFont(QFont("Arial", 12))
        layout.addWidget(self.username_input)

        # Password Input with Toggle Button
        password_layout = QHBoxLayout()
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setFont(QFont("Arial", 12))
        self.password_input.setEchoMode(QLineEdit.Password)

        self.toggle_password_button = QPushButton("👁️")  # Initial emoji set here
        self.toggle_password_button.setCheckable(True)
        self.toggle_password_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.toggle_password_button.setFixedSize(30, 30)
        self.toggle_password_button.setStyleSheet(
            "border: none; background: transparent; padding: 5px;"
        )
        self.toggle_password_button.clicked.connect(self.toggle_password_visibility)

        password_layout.addWidget(self.password_input)
        password_layout.addWidget(self.toggle_password_button)
        layout.addLayout(password_layout)

        # Remember Me Checkbox
        self.remember_me_checkbox = QCheckBox("Remember me")
        layout.addWidget(self.remember_me_checkbox)

        # Login Button
        login_button = QPushButton("Login")
        login_button.setFont(QFont("Arial", 12, QFont.Bold))
        login_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px;")
        login_button.clicked.connect(self.handle_login)
        layout.addWidget(login_button)

        # Signup Link
        signup_label = QLabel('<a href="#">Belum memiliki akun? Daftar di sini</a>')
        signup_label.setFont(QFont("Arial", 10))
        signup_label.setAlignment(Qt.AlignCenter)
        signup_label.setOpenExternalLinks(False)
        signup_label.setCursor(QCursor(Qt.PointingHandCursor))
        signup_label.linkActivated.connect(self.handle_signup)
        layout.addWidget(signup_label)

        # Status Label
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: red; font-size: 12px;")
        layout.addWidget(self.status_label)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        # Dummy authentication for demonstration purposes
        if username == "admin" and password == "123":
            QMessageBox.information(self, "Login Successful", "Welcome, admin!")
        else:
            self.status_label.setText("Incorrect username or password. Try again.")

    def handle_signup(self):
        QMessageBox.information(self, "Signup", "Redirecting to signup page...")  # Example action

    def toggle_password_visibility(self):
        if self.toggle_password_button.isChecked():
            self.password_input.setEchoMode(QLineEdit.Normal)
            self.toggle_password_button.setText("🙈")  # Icon or text for "Hide"
        else:
            self.password_input.setEchoMode(QLineEdit.Password)
            self.toggle_password_button.setText("👁️")  # Icon or text for "Show"


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("assets/ikon_saya.ico"))

    # Create main window
    login_form = LoginForm()
    login_form.show()

    sys.exit(app.exec())
