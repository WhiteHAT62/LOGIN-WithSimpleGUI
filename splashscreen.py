from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QSplashScreen
from PySide6.QtCore import Qt, QTimer

class SplashScreen(QSplashScreen):
    def __init__(self):
        super().__init__()
        # Set splash image
        pixmap = QPixmap("assets/ikon_saya.png").scaled(250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.setPixmap(pixmap)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.showMessage(
            "Loading...",
            Qt.AlignBottom | Qt.AlignCenter,
            Qt.white
        )

    def show_splash(self, duration=3000):
        self.show()
        QTimer.singleShot(duration, self.close)