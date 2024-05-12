from PySide6.QtWidgets import QMainWindow, QWidget, QPushButton,QLabel, QVBoxLayout, QComboBox, QSizePolicy, QMenu, QHBoxLayout, QStackedWidget
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QPalette, QIcon,QPixmap
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
    
    def __init__(self, title: str = "Emissions de GES par types de localités", test=True) -> None:
        super().__init__()
        self.setWindowTitle(title)
        self.setMinimumSize(800,600)
        self.api = Api()
        self.map = Map(self.api)
        self.dataname = "Communes"

        self.test = test
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.central_layout = QVBoxLayout(self.central_widget)
        self.central_layout.setContentsMargins(20, 20, 20, 20)
        self.central_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.menu = QMenu(self)
        self.menu.addAction("Générer une carte", self.__showMap)
        self.menu.addAction("Générer des graphiques", self.__show_graphic)

        self.menu_button = QPushButton("Menu", self)
        self.menu_button.setMenu(self.menu)
        self.menu_button.setFixedSize(100, 30)
        self.menu_button.setIcon(QIcon(f"{RESOURCE_PATH}\\icons\\icon-x32.ico").pixmap(30,30))

        self.central_layout.addWidget(self.menu_button)

        self.stacked_widget = QStackedWidget()

        self.graph_page = QWidget()
        self.stacked_widget.addWidget(self.graph_page)

        self.map_page = QWidget()
        self.stacked_widget.addWidget(self.map_page)

        self.accueil_page = QWidget()
        self.stacked_widget.addWidget(self.accueil_page)
        
        self.setup_accueil_page()
        self.setup_map_page()
        self.setup_graph_page()

    def setup_accueil_page(self):
        accueil_page = QWidget()
        layout = QVBoxLayout(accueil_page)
        layout.setContentsMargins(0, 0, 0, 0)

        background_label = QLabel(accueil_page)
        pixmap = QPixmap(f"{RESOURCE_PATH}\\background\\accueil.png")
        background_label.setPixmap(pixmap)
        background_label.setScaledContents(True)

        layout.addWidget(background_label)
        self.central_layout.addWidget(accueil_page)

    def setup_map_page(self):

        layout = QVBoxLayout(self.map_page)
        self.map_view = QWebEngineView()
        file_path = abspath("map.html")
        self.map_view.settings().setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        self.map_view.setUrl(QUrl.fromLocalFile(file_path))
        layout.addWidget(self.map_view)

    def setup_graph_page(self):
        """Configurer les éléments de la page du graphique"""

        layout = QVBoxLayout(self.graph_page)
        button_layout = QHBoxLayout()

        # Créer une combobox principale
        self.list_ville = QComboBox(self)
        self.list_ville.addItems(["Choisissez le type de localité","Commune", "Région", "Département"])
        self.list_ville.setStyleSheet("QComboBox { min-width: 200px; }")  # Définir une largeur minimale
        self.list_ville.currentIndexChanged.connect(self.on_main_combo_box_changed)
        layout.addWidget(self.list_ville, alignment=Qt.AlignmentFlag.AlignHCenter)  # Centrer la combobox horizontalement

        # Créer un bouton pour générer les graphiques
        button_layout.addStretch(1)
        self.generate_graph_button = QPushButton("Générer le graphique", self)
        self.generate_graph_button.setFixedSize(150, 30)
        self.generate_graph_button.clicked.connect(self.__generate_graph)
        button_layout.addWidget(self.generate_graph_button)

        # Créer un bouton pour enregistrer les graphiques
        self.save_button = QPushButton("Enregistrer le graphique", self)
        self.save_button.setFixedSize(150, 30)
        self.save_button.clicked.connect(self.save_graph)
        button_layout.addWidget(self.save_button)

        # Ajouter un étirement flexible
        button_layout.addStretch(1)
        layout.addLayout(button_layout)

        # Créer le FigureCanvas pour afficher le graphique
        self.figure = Figure()
        self.figure.set_facecolor(self.graph_page.palette().color(QPalette.ColorRole.Window).name()) # Mettre le fond du canvas a la même couleur que le fond du menu
        self.canvas: FigureCanvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas, alignment=Qt.AlignCenter)
        self.canvas.setMaximumSize(1200, 900)  # Augmenter la largeur et la hauteur maximales du canevas
        self.canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)  # Ajuster la politique de taille du canevas pour qu'il puisse s'étendre

    def on_main_combo_box_changed(self):
        self.save_button.clicked.disconnect(self.save_graph)
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
        self.figure.savefig(f"bilan_GES_{self.dataname[0:-1]}_{self.list_ville.currentText()}")

    def __showMap(self):
        self.stacked_widget.setCurrentWidget(self.map_page)

    def __show_graphic(self):
        self.stacked_widget.setCurrentWidget(self.graph_page)
    
    def __generate_graph(self):
        selected_text = self.list_ville.currentText()
        if selected_text not in ["Retour","Commune", "Région", "Département","Choisissez le type de localité"]:
            inputdata = selected_text
            data = self.api.getCO2(self.dataname, inputdata)
            dates = list(data.keys())
            totalco2 = list(data.values())

            self.figure.clear()
            ax = self.figure.subplots()
            ax.bar(dates, totalco2, label="CO2")
            ax.set_title(f"Bilan GES, {self.dataname[0:-1]} : {inputdata}", color="white")
            ax.set_xlabel('Dates',  color="white")
            ax.set_ylabel('Tonnes de CO2',  color="white")
            ax.legend()
            ax.tick_params(axis='x', rotation=90)
            ax.tick_params(labelcolor='white')

            self.figure.subplots_adjust(bottom=0.25)
            self.canvas.draw()
            self.save_button.clicked.connect(self.save_graph)