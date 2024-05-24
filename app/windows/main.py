"""
Interface principale
"""

from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QStackedWidget
from PySide6.QtGui import QIcon
from requests.exceptions import HTTPError
from PySide6.QtMultimedia import QSoundEffect
from PySide6.QtCore import QThread, QUrl

from app.components.messagebox import MessageBox
from app.components.sidebar import SideBar
from app.components.pages.home import HomePage
from app.components.pages.graph import GraphPage
from app.components.pages.map import MapPage
from utils.palette import Palette
from utils.api import Api
from utils.map import Map
from utils.constants import RESOURCE_PATH

class Main(QMainWindow):
    """
    Classe Main pour générer l'interface principale
    """

    # Initialisation (constructeur)
    def __init__(self, title: str) -> None:
        super().__init__()
        
        # Initialisation de la base (icone, titre)
        self.setWindowIcon(QIcon(f"{RESOURCE_PATH}\\icons\\icon-x32.ico"))
        self.setWindowTitle(title)
        self.setMinimumSize(800,600)

        # Palette de couleur par défaut (comme ca tout le monde a les même couleurs)
        self.setPalette(Palette())

        # Initialisation du module API
        try:
            api = Api()
        except HTTPError as e:
            MessageBox.show(title="Erreur", text=f"Erreur de requête vers l'API: {e.response}")

        # Initialisation du module carte
        map = Map(api)

        # Créer un widget central pour la fenêtre
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Créer un layout vertical pour le widget central
        central_layout = QHBoxLayout()
        central_layout.setContentsMargins(0, 0, 0, 0)
        central_layout.setSpacing(0)
        central_widget.setLayout(central_layout)

        # Widget pour gérer les pages
        page_manager = QStackedWidget(self)

        # Liste des pages
        pages = [
            HomePage(parent=page_manager),
            GraphPage(api=api, parent=page_manager),
            MapPage(map=map, parent=page_manager)
        ]

        for page in pages:
            page_manager.addWidget(page)

        # Widget sidebar
        sidebar = SideBar(page_manager=page_manager, parent=self)
        central_layout.addWidget(sidebar)

        central_layout.addWidget(page_manager)

        #self.play_sound()