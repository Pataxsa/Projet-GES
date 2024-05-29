"""
Page map

Module :
    PySide6.QtWidgets.QWidget : Classe de base des objets QtWidgets
    PySide6.QtWidgets.QVBoxLayout : Pour placer les éléments verticalement (les uns au-dessus des autres)
    PySide6.QtCore.QUrl : Classe pour gérer les URLs (de la map)
    PySide6.QtWebEngineCore.QWebEngineSettings : Pour configurer la page de la map "comme un site" 
    PySide6.QtWebEngineWidgets.QWebEngineView : Pour pouvoir voir la map dans la page (site)
    
    abspath : Pour obtenir le chemin absolu d'un fichier
    ROOT_PATH : Import la variable ROOT_PATH depuis utils.constants
    Map : Importe la classe Map
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtGui import QFont
from os.path import abspath
from PySide6.QtCore import QUrl, Qt
from PySide6.QtWebEngineCore import QWebEngineSettings
from PySide6.QtWebEngineWidgets import QWebEngineView

from utils import Map
from utils.constants import ROOT_PATH

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
        self.map_view = None

    # Evenement lorsque la page est affichée
    def showEvent(self, event):
        if not self.map_view:
            self.map.save(f"{ROOT_PATH}\\tmp\\map.html")
            self.progress_label = QLabel(parent=self, text=f"0%")
            self.progress_label.setFont(QFont("Arial", 24))
            self.progress_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.layout().addWidget(self.progress_label)
            self.map_view = QWebEngineView()
            self.map_view.loadProgress.connect(self.__load_progress)
            file_path = abspath(f"{ROOT_PATH}\\tmp\\map.html")
            self.map_view.settings().setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
            self.map_view.setUrl(QUrl.fromLocalFile(file_path))
    
    # Evenement qui s'actualise lorsque lorsque le QWebEngineView se charge
    def __load_progress(self, progress):
        self.progress_label.setText(f"{progress}%")
        
        if progress == 100:
            self.layout().removeWidget(self.progress_label)
            del self.progress_label
            self.layout().addWidget(self.map_view)
            self.map.delete(f"{ROOT_PATH}\\tmp\\map.html")
