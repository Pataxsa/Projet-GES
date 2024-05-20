"""
Page home
"""

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

from utils.constants import RESOURCE_PATH

class HomePage(QWidget):
    """
    Classe HomePage pour générer la page home
    """

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)

        # Layout principal
        central_layout = QVBoxLayout()
        central_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(central_layout)

        # Image
        image = QLabel(self)
        pixmap = QPixmap(f"{RESOURCE_PATH}\\images\\accueil.jpg")
        image.setPixmap(pixmap)
        image.setScaledContents(True)
        central_layout.addWidget(image)
