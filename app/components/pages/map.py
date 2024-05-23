"""
Page map

Module :
    PySide6.QtWidgets.QWidget : Classe de base des objets QtWidgets
    PySide6.QtWidgets.QVBoxLayout : Pour placer les éléments verticalement (les uns au-dessus des autres)
    PySide6.QtCore.QUrl : Classe pour gérer les URLs (de la map)
    PySide6.QtWebEngineCore.QWebEngineSettings : Pour configurer la page de la map "comme un site" 
    PySide6.QWebEngineWidgets.QWebEngineView : Pour pouvoir voir la map dans la page (site)
    
    abspath : Pour obtenir le chemin absolu d'un fichier
    ROOT_PATH : Import la variable ROOT_PATH depuis utils.constants
    Map : Importe la classe Map
"""

from PySide6.QtWidgets import QWidget,QVBoxLayout
from os.path import abspath
from PySide6.QtCore import QUrl
from PySide6.QtWebEngineCore import QWebEngineSettings
from PySide6.QtWebEngineWidgets import QWebEngineView

from utils.constants import ROOT_PATH
from utils.map import Map

class MapPage(QWidget):
    """
    Classe MapPage pour générer la page map
    """

    def __init__(self, map: Map, parent: QWidget = None) -> None:
        super().__init__(parent)

        # Carte
        self.map = map

        # Layout principal
        central_layout = QVBoxLayout(self)
        central_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(central_layout)

        # Map View
        # TODO: Pas opti (pour opti il ne faut pas le charger au démarrage)
        self.map_view = QWebEngineView()
        file_path = abspath(f"{ROOT_PATH}\\map.html")
        self.map_view.settings().setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        self.map_view.setUrl(QUrl.fromLocalFile(file_path))
        central_layout.addWidget(self.map_view)
