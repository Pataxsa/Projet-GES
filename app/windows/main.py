from PySide6.QtWidgets import QMainWindow, QWidget, QPushButton, QVBoxLayout, QComboBox, QSizePolicy, QMenu, QHBoxLayout, QStackedWidget
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QPalette, QIcon
from PySide6.QtWebEngineCore import QWebEngineSettings
from PySide6.QtWebEngineWidgets import QWebEngineView
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from os.path import abspath

from utils.api import Api
from utils.map import Map
from utils.constants import RESOURCE_PATH

class Main(QMainWindow):
    """
    Classe Main pour générer l'interface principale
    """
    
    # Initialisation (constructeur)
    def __init__(self, title: str = "Emissions de GES par types de localités", test=True) -> None:
        super().__init__()
        self.setWindowTitle(title)
        self.setMinimumSize(800,600) #pas de pb avec les redimensionnements
        self.api = Api()
        self.map = Map(self.api)
        self.dataname = "Communes"

        self.test = test
        # Créer un widget central pour la fenêtre
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Créer un layout vertical pour le widget central
        self.central_layout = QVBoxLayout(central_widget)
        self.central_layout.setContentsMargins(20, 20, 20, 20)
        self.central_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Centrer les éléments verticalement

        # Créer un menu pour afficher les options
        self.menu = QMenu(self)

        # Ajouter les actions au menu
        self.menu.addAction("Générer une carte", self.__showMap)
        self.menu.addAction("Générer des graphiques", self.__show_graphic)

        # Créer un bouton pour le menu
        self.menu_button = QPushButton("Menu", self)
        self.menu_button.setMenu(self.menu)
        self.menu_button.setFixedSize(100, 30)
        self.menu_button.setIcon(QIcon(f"{RESOURCE_PATH}\\icons\\icon-x32.ico").pixmap(30,30))

        # Ajouter le bouton en haut à gauche
        self.central_layout.addWidget(self.menu_button)

        # Créer une combobox principale
        self.list_ville = QComboBox(self)
        self.list_ville.addItems(["Choisissez le type de localité","Commune", "Région", "Département"])
        self.list_ville.setStyleSheet("QComboBox { min-width: 200px; }")  # Définir une largeur minimale
        self.list_ville.currentIndexChanged.connect(self.on_main_combo_box_changed)

        self.central_layout.addWidget(self.list_ville, alignment=Qt.AlignmentFlag.AlignHCenter)  # Centrer la combobox horizontalement

        # Créer un stacked widget pour gérer les pages
        self.stacked_widget = QStackedWidget()
        self.central_layout.addWidget(self.stacked_widget)

        # Créer les pages et les ajouter au stacked widget
        self.map_page = QWidget()
        self.stacked_widget.addWidget(self.map_page)

        self.graph_page = QWidget()
        self.stacked_widget.addWidget(self.graph_page)

        # Afficher initialement la page de la carte
        self.stacked_widget.setCurrentWidget(self.map_page)

        # Créer les éléments pour la page de la carte
        self.setup_map_page()

        # Créer les éléments pour la page du graphique
        self.setup_graph_page()

    def setup_map_page(self):
        """Configurer les éléments de la page de la carte"""
        layout = QVBoxLayout(self.map_page)
        self.map_view = QWebEngineView()
        file_path = abspath("map.html")
        self.map_view.settings().setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        self.map_view.setUrl(QUrl.fromLocalFile(file_path))
        layout.addWidget(self.map_view)

    def setup_graph_page(self):
        """Configurer les éléments de la page du graphique"""
        layout = QVBoxLayout(self.graph_page)

        # Créer le FigureCanvas pour afficher le graphique
        self.figure = Figure()
        self.figure.set_facecolor(self.graph_page.palette().color(QPalette.ColorRole.Window).name()) # Mettre le fond du canvas a la même couleur que le fond du menu
        self.canvas: FigureCanvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        self.canvas.setMaximumSize(1000, 800) # Taille max du canvas
        self.canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding) # Fait en sorte que le canvas puisse s'étendre

    def on_main_combo_box_changed(self):
        
        selected_text = self.list_ville.currentText()

        match selected_text:
            case "Région" | "Département" | "Commune":
                values = ["Retour"]
                values.extend(self.api.locality_names[f"{selected_text.replace("é", "e")}s"])
                self.dataname = f"{selected_text}s"
                self.list_ville.currentIndexChanged.disconnect(self.on_main_combo_box_changed)
                self.list_ville.clear()
                self.list_ville.addItems(values)
                self.list_ville.setCurrentIndex(1)
                self.list_ville.currentIndexChanged.connect(self.on_main_combo_box_changed)
            case "Retour":
                self.list_ville.clear()
                self.list_ville.addItems(["Choisissez le type de localité", "Commune", "Région", "Département"])
    
    def save_graph(self):
        if not self.test:
            self.figure.savefig(f"bilan_GES_{self.dataname[0:-1]}_{self.list_ville.currentText()}")

    def __showMap(self):
        """Afficher la page de la carte"""
        self.stacked_widget.setCurrentWidget(self.map_page)

    def __show_graphic(self):
        """Afficher la page du graphique"""
        self.stacked_widget.setCurrentWidget(self.graph_page)