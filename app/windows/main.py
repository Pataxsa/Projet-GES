"""
Interface principale
"""

from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QStackedWidget
from PySide6.QtGui import QIcon
from requests.exceptions import HTTPError

from app.components.messagebox import MessageBox
from app.components.sidebar import SideBar
from app.components.pages.home import HomePage
from app.components.pages.graph import GraphPage
from app.components.pages.map import MapPage
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
        
        self.setWindowIcon(QIcon(f"{RESOURCE_PATH}\\icons\\icon-x32.ico"))
        self.setWindowTitle(title)
        self.setMinimumSize(800,600) #pas de pb avec les redimensionnements

        # Initialisation de l'API
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

        # Liste de pages
        pages = [
            HomePage(self),
            GraphPage(api, self),
            MapPage(map, self)
        ]

        # Widget pour gérer les pages
        page_manager = QStackedWidget(self)
        for page in pages:
            page_manager.addWidget(page)

        # Widget sidebar
        sidebar = SideBar(page_manager, self)
        central_layout.addWidget(sidebar)

        central_layout.addWidget(page_manager)
