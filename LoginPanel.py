import sys
import PySide6.QtWidgets
from PySide6.QtGui import QFont, QCursor, QIcon, QPalette, QColor, QPixmap, QMouseEvent
from PySide6.QtCore import Qt

loading_screen_shown = False

class LoginForm(PySide6.QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PASSWORD MANAGER")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setFixedSize(500, 340)
        self.setAttribute(Qt.WA_TranslucentBackground, False)

        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#1E1E2C"))
        palette.setColor(QPalette.WindowText, QColor("#8F94FB"))
        self.setPalette(palette)

        self.offset = None
        self.setup_ui()

    def setup_ui(self):
        main_layout = PySide6.QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Custom title bar
        title_bar = PySide6.QtWidgets.QWidget()
        title_bar.setFixedHeight(40)
        title_bar.setStyleSheet("background-color: #2A2A40;")
        title_layout = PySide6.QtWidgets.QHBoxLayout(title_bar)
        title_layout.setContentsMargins(10, 0, 10, 0)

        icon_label = PySide6.QtWidgets.QLabel()
        icon_pixmap = QPixmap("assets/ikon.ico").scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        icon_label.setPixmap(icon_pixmap)
        title_layout.addWidget(icon_label)

        title_text = PySide6.QtWidgets.QLabel("PASSWORD MANAGER")
        title_text.setStyleSheet("color: white; font-weight: bold;")
        title_layout.addWidget(title_text)
        title_layout.addStretch()

        minimize_button = PySide6.QtWidgets.QPushButton("⛔️")
        minimize_button.setFixedSize(30, 30)
        minimize_button.setFont(QFont("Arial", 14))
        minimize_button.setStyleSheet("""
                    QPushButton {
                        color: white;
                        background: none;
                        border: none;
                    }
                    QPushButton:hover {
                        background-color: #44475a;
                    }
                """)
        minimize_button.clicked.connect(self.showMinimized)
        title_layout.addWidget(minimize_button)

        close_button = PySide6.QtWidgets.QPushButton("❌")
        close_button.setFixedSize(30, 30)
        close_button.setFont(QFont("Arial", 14))
        close_button.setStyleSheet("""
                    QPushButton {
                        color: white;
                        background: none;
                        border: none;
                    }
                    QPushButton:hover {
                        background-color: #44475a;
                    }
                """)
        close_button.clicked.connect(self.close)
        title_layout.addWidget(close_button)

        title_bar.mousePressEvent = self.mousePressEvent
        title_bar.mouseMoveEvent = self.mouseMoveEvent

        main_layout.addWidget(title_bar)

        # Main login UI
        container = PySide6.QtWidgets.QWidget()
        container_layout = PySide6.QtWidgets.QVBoxLayout(container)
        container_layout.setContentsMargins(50, 0, 50, 0)

        title_label = PySide6.QtWidgets.QLabel("Welcome Back!")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setStyleSheet("margin-top: 15px")
        title_label.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(title_label)

        self.username_input = PySide6.QtWidgets.QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setFont(QFont("Arial", 12))
        self.username_input.setStyleSheet("background: #2A2A40; color: white; margin-top: 15px")
        container_layout.addWidget(self.username_input)

        password_layout = PySide6.QtWidgets.QHBoxLayout()
        self.password_input = PySide6.QtWidgets.QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setFont(QFont("Arial", 12))
        self.password_input.setStyleSheet("background: #2A2A40; color: white;")
        self.password_input.setEchoMode(PySide6.QtWidgets.QLineEdit.Password)

        self.toggle_password_button = PySide6.QtWidgets.QPushButton("👁️")
        self.toggle_password_button.setCheckable(True)
        self.toggle_password_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.toggle_password_button.setFixedSize(30, 30)
        self.toggle_password_button.setFont(QFont("Arial", 15))
        self.toggle_password_button.setStyleSheet("border: none; background: #2A2A40; padding: 5px; border-radius: 4px")
        self.toggle_password_button.clicked.connect(self.toggle_password_visibility)

        password_layout.addWidget(self.password_input)
        password_layout.addWidget(self.toggle_password_button)
        container_layout.addLayout(password_layout)

        self.remember_me_checkbox = PySide6.QtWidgets.QCheckBox("Remember me")
        self.remember_me_checkbox.setStyleSheet("color: #B0B0C3;")
        container_layout.addWidget(self.remember_me_checkbox)

        login_button = PySide6.QtWidgets.QPushButton("Login")
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
        container_layout.addWidget(login_button)

        signup_label = PySide6.QtWidgets.QLabel('<a href="#">Belum memiliki akun? Daftar di sini</a>')
        signup_label.setFont(QFont("Arial", 10))
        signup_label.setAlignment(Qt.AlignCenter)
        signup_label.setStyleSheet("color: #00D9FF;")
        signup_label.setOpenExternalLinks(False)
        signup_label.setCursor(QCursor(Qt.PointingHandCursor))
        signup_label.linkActivated.connect(self.handle_signup)
        container_layout.addWidget(signup_label)

        self.status_label = PySide6.QtWidgets.QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: red; font-size: 12px;")
        container_layout.addWidget(self.status_label)

        main_layout.addWidget(container)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if username == "admin" and password == "123":
            PySide6.QtWidgets.QMessageBox.information(self, "Login Successful", "Welcome, admin!")
        else:
            self.status_label.setText("Incorrect username or password. Try again.")

    def handle_signup(self):
        PySide6.QtWidgets.QMessageBox.information(self, "Signup", "Redirecting to signup page...")

    def toggle_password_visibility(self):
        if self.toggle_password_button.isChecked():
            self.password_input.setEchoMode(PySide6.QtWidgets.QLineEdit.Normal)
            self.toggle_password_button.setText("🙈")
        else:
            self.password_input.setEchoMode(PySide6.QtWidgets.QLineEdit.Password)
            self.toggle_password_button.setText("👁️")

        # Custom move window with mouse drag

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.offset = event.globalPosition().toPoint() - self.pos()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.offset and event.buttons() == Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self.offset)

if __name__ == "__main__":
    app = PySide6.QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QIcon("assets/ikon.ico"))

    if not globals().get("loading_screen_shown", False):
        from hello import LoadingScreen
        loading_screen_shown = True
        loading_screen = LoadingScreen()
        loading_screen.show()
        sys.exit(app.exec())
    else:
        login_panel = LoginForm()
        login_panel.show()
        sys.exit(app.exec())
