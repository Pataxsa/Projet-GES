"""
Page map
"""

#TODO: continuer

from PySide6.QtWidgets import QWidget,QVBoxLayout
from os.path import abspath
from PySide6.QtCore import QUrl
from PySide6.QtWebEngineCore import QWebEngineSettings
from PySide6.QtWebEngineWidgets import QWebEngineView

from utils.map import Map

class MapPage(QWidget):
    """
    Classe MapPage pour générer la page map
    """

    def __init__(self, map: Map, parent: QWidget = None) -> None:
        super().__init__(parent)
        # Carte
        self.map = map
        layout = QVBoxLayout(self)
        self.map_view = QWebEngineView()
        file_path = abspath("map.html")
        self.map_view.settings().setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        self.map_view.setUrl(QUrl.fromLocalFile(file_path))
        layout.addWidget(self.map_view)
