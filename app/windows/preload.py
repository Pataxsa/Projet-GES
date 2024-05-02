"""
Interface préchargement
"""

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QApplication, QProgressBar

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

        self.show()

    def update(self, text: str, percent: int) -> None:
        """
        Fonction update qui actualise le texte et la barre de progression
        """

        self.label.setText(text)
        self.progressbar.setValue(percent)
        QApplication.processEvents()
