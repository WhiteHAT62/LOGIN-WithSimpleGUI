import sys
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QIcon, QPixmap

class LoadingScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.login_panel = None
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setFixedSize(500, 340)
        self.setStyleSheet("background-color: #1E1E2C;")

        self.logo_label = QLabel(self)
        self.logo_label.setPixmap(QPixmap("assets/ikon_saya.png"))
        self.logo_label.setScaledContents(True)
        self.logo_label.setGeometry(210, 120, 100, 100)

        QTimer.singleShot(2000, self.open_login_panel) 

    def open_login_panel(self):
        self.close()
        from login import LoginForm 
        self.login_panel = LoginForm()
        self.login_panel.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("assets/ikon.ico"))
    loading_screen = LoadingScreen()
    loading_screen.show()
    sys.exit(app.exec())