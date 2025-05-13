import os
import sqlite3
import sys

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QMainWindow
from PySide6.QtGui import Qt, QFont, QPixmap
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QFrame, QSizePolicy

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class TitleBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setFixedSize(600, 40)
        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("background-color: #2A2A40;")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        icon = QLabel()
        icon_pixmap = QPixmap(resource_path("assets/ikon.ico")).scaled(20, 20, Qt.KeepAspectRatio,
                                                                       Qt.SmoothTransformation)
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

class HalamanUtama(QMainWindow):
    logout_signal = Signal()
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Window)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(600, 400)

        self.container = QWidget()
        self.container.setStyleSheet("background: #1E1E2C")
        self.setCentralWidget(self.container)

        layout_utama = QVBoxLayout(self.container)
        layout_utama.setContentsMargins(0, 0, 0, 0)
        layout_utama.setSpacing(0)

        self.title_bar = TitleBar(self)
        layout_utama.addWidget(self.title_bar)

        label_container = QWidget()
        label_container_layout = QVBoxLayout(label_container)
        label_container_layout.setContentsMargins(15, 15, 15, 10)
        label_container_layout.setSpacing(5)

        conn = sqlite3.connect("main.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        conn.close()

        self.nama = user[0]
        label_sapaan = QLabel(f"HI {self.nama}!")
        label_sapaan.setFont(QFont("Segoe UI", 16, QFont.Bold))
        label_sapaan.setStyleSheet("color: white;")
        label_container_layout.addWidget(label_sapaan)

        label_deskripsi = QLabel("saat ini anda berada di tempat penyimpanan paling aman di dunia")
        label_deskripsi.setFont(QFont("Arial", 10))
        label_deskripsi.setStyleSheet("color: white;")
        label_container_layout.addWidget(label_deskripsi)

        layout_utama.addWidget(label_container)

        main_container = QWidget()
        main_container_layout = QVBoxLayout(main_container)
        main_container_layout.setContentsMargins(15, 0, 15, 15)

        main_frame = QFrame()
        main_frame.setStyleSheet("background-color: #2A2A40; border-radius: 10px;")
        main_container_layout.addWidget(main_frame)

        layout_utama.addWidget(main_container, stretch=1)

        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()
        logout_button = QPushButton("LogOut")
        logout_button.setStyleSheet("""
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
        logout_button.clicked.connect(self.handle_logout)
        bottom_layout.addWidget(logout_button)
        bottom_layout.setContentsMargins(0, 0, 15, 15)

        layout_utama.addLayout(bottom_layout)

    def handle_logout(self):
        from Main import clear_remember_me_token
        clear_remember_me_token()
        self.logout_signal.emit()
        self.close()



