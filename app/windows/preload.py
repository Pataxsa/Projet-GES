"""
Interface préchargement
"""

from PySide6.QtCore import Qt, QUrl, QThread
from PySide6.QtMultimedia import QSoundEffect
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QProgressBar,QMainWindow
from utils.constants import RESOURCE_PATH

class Preload(QMainWindow):
    """
    Classe Preload pour générer le splash screen (interface)
    """

    # Initialisation (constructeur)
    def __init__(self, text: str, percent: int) -> None:
        super().__init__()

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.ToolTip)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedHeight(200)
        self.setFixedWidth(300)

        # Fenetre
        central_widget = QWidget()
        central_widget.setObjectName("Window")
        central_widget.setStyleSheet("#Window { background: QLinearGradient(x1:0 y1:0, x2:1 y2:1, stop:0 #051c2a stop:1 #44315f); border-radius: 10px; }")
        self.setCentralWidget(central_widget)

        # Layout
        central_layout = QVBoxLayout()
        central_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        central_layout.setSpacing(20)
        central_widget.setLayout(central_layout)

        # Texte
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.label.setFont(QFont('Arial', 14))
        self.label.setStyleSheet("color: white")
        central_layout.addWidget(self.label)

        # Barre de progression
        self.progressbar = QProgressBar(self)
        self.progressbar.setFixedSize(240, 30)
        self.progressbar.setFont(QFont('Arial', 10))
        self.progressbar.setStyleSheet("""
                                        QProgressBar { 
                                            text-align: center; 
                                            color: black; 
                                            background-color: white; 
                                            border-radius: 7px; 
                                        } 
                                       
                                        QProgressBar::chunk { 
                                            background-color: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #78d, stop: 0.5 #45a, stop: 1 #238 ); 
                                            border-radius: 4px; 
                                        }
                                       """)
        central_layout.addWidget(self.progressbar)

        self.play_sound() # JOUER LE SON A L'OUVERTURE
        self.show()

    def update(self, text: str, percent: int) -> None:
        """
        Fonction update qui actualise le texte et la barre de progression
        """

        self.label.setText(text)
    

    def play_sound(self):
        self.sound_effect = QSoundEffect()
        self.sound_effect.setSource(QUrl.fromLocalFile(f"{RESOURCE_PATH}\\sounds\\loading_sound.wav"))

        self.thread_worker = QThread()
        self.thread_worker.started.connect(self.sound_effect.play)
        self.sound_effect.statusChanged.connect(self.thread_worker.quit)
        self.thread_worker.start()

    def closeEvent(self, event):
        self.thread_worker.quit()