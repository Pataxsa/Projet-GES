"""
Page map
"""

#TODO: continuer

from PySide6.QtWidgets import QWidget

from utils.map import Map

class MapPage(QWidget):
    """
    Classe MapPage pour générer la page map
    """

    def __init__(self, map: Map, parent: QWidget = None) -> None:
        super().__init__(parent)

        # Carte
        self.map = map
