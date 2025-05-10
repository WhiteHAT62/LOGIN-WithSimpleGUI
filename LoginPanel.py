import sys

from PySide6.QtWidgets import QLineEdit

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QMessageBox,
    QWidget, QLabel, QHBoxLayout, QVBoxLayout,
    QPushButton, QStyle, QSizePolicy, QSplashScreen, QFrame
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QCursor, QIcon, QPalette, QColor, QPixmap, QMouseEvent, QPainter

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
        icon_pixmap = QPixmap("assets/ikon.ico").scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation)
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
            try:
                if hasattr(self.parent, 'windowHandle') and self.parent.windowHandle():
                    self.parent.windowHandle().startSystemMove()
                event.accept()
            except Exception as e:
                if hasattr(self.parent, 'windowHandle') and self.parent.windowHandle():
                    delta = event.globalPos() - self.drag_start_position
                    self.parent.move(self.parent.pos() + delta)
                    self.drag_start_position = event.globalPos()
                    event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton and hasattr(self, 'drag_start_position'):
            delta = event.globalPos() - self.drag_start_position
            self.parent.move(self.parent.pos() + delta)
            self.drag_start_position = event.globalPos()
            event.accept()

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
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

        #Tambahkan disini
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText(" Username")
        self.username_input.setFont(QFont("Arial", 12))
        self.username_input.setStyleSheet("background: #2A2A40; color: white; margin-top: 15px")
        self.username_input.returnPressed.connect(self.handle_login)
        content_layout.addWidget(self.username_input)

        password_layout = QHBoxLayout()
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText(" Password")
        self.password_input.setFont(QFont("Arial", 12))
        self.password_input.setStyleSheet("background: #2A2A40; color: white;")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.returnPressed.connect(self.handle_login)

        self.toggle_password_button = QPushButton("👁️")
        self.toggle_password_button.setCheckable(True)
        self.toggle_password_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.toggle_password_button.setFixedSize(30, 30)
        self.toggle_password_button.setFont(QFont("Arial", 15))
        self.toggle_password_button.setStyleSheet("border: none; background: #2A2A40; padding: 5px; border-radius: 4px")
        self.toggle_password_button.clicked.connect(self.toggle_password_visibility)

        password_layout.addWidget(self.password_input)
        password_layout.addWidget(self.toggle_password_button)
        content_layout.addLayout(password_layout)

        from PySide6.QtWidgets import QCheckBox  # Tambahkan ini kalau belum di bagian atas
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

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if username == "admin" and password == "123":
            QMessageBox.information(self, "Login Successful", "Welcome, admin!")
        else:
            self.status_label.setText("Incorrect username or password. Try again.")

    def handle_signup(self):
        QMessageBox.information(self, "Signup", "Redirecting to signup page...")

    def toggle_password_visibility(self):
        if self.toggle_password_button.isChecked():
            self.password_input.setEchoMode(QLineEdit.Normal)
            self.toggle_password_button.setText("🙈")
        else:
            self.password_input.setEchoMode(QLineEdit.Password)
            self.toggle_password_button.setText("👁️")


def show_login():
    window = LoginWindow()
    splash.close()
    window.show()

def add_padding_to_pixmap(pixmap, padding_bottom):
    new_height = pixmap.height() + padding_bottom
    padded_pixmap = QPixmap(pixmap.width(), new_height)
    padded_pixmap.fill(Qt.transparent)

    painter = QPainter(padded_pixmap)
    painter.drawPixmap(0, 0, pixmap)
    painter.end()

    return padded_pixmap

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("assets/ikon_saya.png"))

    original_pix = QPixmap("assets/ikon_saya.png").scaled(300, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    splash_pix = add_padding_to_pixmap(original_pix, 10)
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setFont(QFont("Arial", 12))
    splash.showMessage("Memuat aplikasi...", Qt.AlignBottom | Qt.AlignCenter, Qt.white)
    splash.show()

    # Delay 2 detik sebelum tampilkan login window
    QTimer.singleShot(2000, show_login)
    sys.exit(app.exec())
