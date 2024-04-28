import sys
from PyQt6.QtCore import QUrl
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
from PySide6.QtMultimedia import QSoundEffect


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Jouer un son")
        self.setGeometry(100, 100, 400, 200)

        self.button = QPushButton("Jouer un son", self)
        self.button.setGeometry(150, 80, 100, 30)
        self.button.clicked.connect(self.play_sound)

        self.sound_effect = QSoundEffect()
        self.sound_effect.setSource(QUrl.fromLocalFile("greg.wav"))

    def play_sound(self):
        self.sound_effect.play()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())