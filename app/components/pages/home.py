"""
Page home

Module :
    PySide6.QtCore.Qt : Pour les fonctions spécifiques à Qt
    PySide6.QtGui.QPixmap : Pour l'image de fond
    PySide6.QtWidgets.QWidget : Classe de base des objets QtWidgets
    PySide6.QtWidgets.QVBoxLayout : Pour mettre les éléments de manière vertical (les uns au-dessus des autres)
    PySide6.QtWidgets.QLabel : Pour gérer l'affichage, le placement et la taille des éléments sur la page

    RESOURCE_PATH : Chemin d'accès aux ressources
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

        # Chemin, placement, taille et affichage de l'image
        image = QLabel(self)
        pixmap = QPixmap(f"{RESOURCE_PATH}\\images\\accueil.jpg")
        image.setPixmap(pixmap)
        image.setScaledContents(True)
        central_layout.addWidget(image)
