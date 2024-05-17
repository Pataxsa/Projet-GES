"""
Interface préchargement
"""

from PySide6.QtCore import Qt, QUrl, QThread
from PySide6.QtMultimedia import QSoundEffect
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QProgressBar
from utils.constants import RESOURCE_PATH

class Preload(QWidget):
    """
    Classe Preload pour générer le splash screen (interface)
    """

    # Initialisation (constructeur)
    def __init__(self) -> None:
        super().__init__()

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.ToolTip)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedHeight(150)
        self.setFixedWidth(300)

        central_layout = QVBoxLayout()
        central_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        central_layout.setSpacing(20)
        self.setLayout(central_layout)

        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.label.setFont(QFont('Arial', 14))
        central_layout.addWidget(self.label)

        self.progressbar = QProgressBar(self)
        self.progressbar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progressbar.setFont(QFont('Arial', 10))
        self.progressbar.setStyleSheet("QProgressBar::chunk { background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #78d, stop: 0.5 #45a, stop: 1 #238 ); border-radius: 7px; border: 1px solid black; }")
        central_layout.addWidget(self.progressbar)

        self.play_sound() # JOUER LE SON A L'OUVERTURE
        self.show()

    def update(self, text: str, percent: int) -> None:
        """
        Fonction update qui actualise le texte et la barre de progression
        """

        self.label.setText(text)
        self.progressbar.setValue(percent)
    

    def play_sound(self):
        self.sound_effect = QSoundEffect()
        self.sound_effect.setSource(QUrl.fromLocalFile(f"{RESOURCE_PATH}\\sounds\\loading_sound.wav"))

        self.thread_worker = QThread()
        self.thread_worker.started.connect(self.sound_effect.play)
        self.sound_effect.statusChanged.connect(self.thread_worker.quit)
        self.thread_worker.start()

    def closeEvent(self, event):
        self.thread_worker.quit()