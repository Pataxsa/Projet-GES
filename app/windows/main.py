"""
Interface principale
"""

from PySide6.QtWidgets import QMainWindow, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QComboBox, QSizePolicy
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from os.path import isfile
from os import remove
from requests.exceptions import HTTPError
from app.components.messagebox import MessageBox
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

        if isfile("map.html"):
            remove("map.html")
        
        self.setWindowIcon(QIcon(f"{RESOURCE_PATH}\\icons\\icon-x32.ico"))
        self.setWindowTitle(title)
        self.setMinimumSize(800,600) #pas de pb avec les redimensionnements

        # Initialisation de l'API
        try:
            self.api = Api()
        except HTTPError as e:
            MessageBox.show(title="Erreur", text=f"Erreur de requête vers l'API: {e.response}")

        # Initialisation de la carte
        self.map = Map(self.api)

        # Créer un widget central pour la fenêtre
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Créer un layout vertical pour le widget central
        central_layout = QVBoxLayout()
        central_widget.setLayout(central_layout)
        central_layout.setContentsMargins(20, 20, 20, 20)
        central_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Centrer les éléments

        # Créer une combobox principale
        self.list_ville = QComboBox(self)
        self.list_ville.addItems(["Choisissez le type de localité", "Commune", "Région", "Département"])
        self.list_ville.setStyleSheet(" QComboBox { min-width: 200px;  } ")  # Définir une largeur minimale
        self.list_ville.currentIndexChanged.connect(self.__on_combobox_changed)
        self.dataname = None

        central_layout.addWidget(self.list_ville, alignment=Qt.AlignmentFlag.AlignHCenter)  # Centrer la combobox horizontalement

        # Créer un layout horizontal pour les boutons
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        button_layout.setContentsMargins(0, 10, 0, 0)
        button_layout.setSpacing(20)
        central_layout.addLayout(button_layout)

        self.graphic_button = QPushButton("Générer un graphique", self)
        self.map_button = QPushButton("Afficher une carte", self)

        self.graphic_button.setEnabled(False)

        # Ajouter les boutons au layout horizontal
        button_layout.addWidget(self.graphic_button)
        button_layout.addWidget(self.map_button)

        self.graphic_button.setFixedSize(150, 30)
        self.map_button.setFixedSize(150, 30)

        # Associer les fonctions aux boutons
        self.graphic_button.clicked.connect(self.__show_graphic)
        self.map_button.clicked.connect(self.__generatemap)

        # Créer le FigureCanvas pour afficher le graphique
        self.figure: Figure = Figure()
        self.figure.set_facecolor(central_widget.palette().color(QPalette.ColorRole.Window).name()) # Mettre le fond du canvas a la même couleur que le fond du menu
        self.canvas: FigureCanvas = FigureCanvas(self.figure)
        central_layout.addWidget(self.canvas)
        self.canvas.setMaximumSize(1000, 800) # Taille max du canvas
        self.canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding) # Fait en sorte que le canvas puisse s'étendre

    # Crée une carte html et ouvre la carte
    def __generatemap(self) -> None:
        self.map.save("map.html")

    # Affiche un graphique
    def __show_graphic(self) -> None:
        inputdata = self.list_ville.currentText()
        data = self.api.getCO2(self.dataname, inputdata)
        dates = list(data.keys())
        totalco2 = list(data.values())

        # Effacer le contenu précédent du graphique
        self.figure.clear()

        # Récupérer l'axe de la figure
        ax = self.figure.subplots()

        # Créer le graphique
        ax.bar(dates, totalco2, label="CO2")
        ax.set_title(f"Bilan GES, {self.dataname[0:-1]} : {inputdata}", color="white")
        ax.set_xlabel('Dates',  color="white")
        ax.set_ylabel('Tonnes de CO2',  color="white")
        ax.legend()
        ax.tick_params(axis='x', rotation=90)
        ax.tick_params(labelcolor='white')

        # Mettre à jour le graphique dans le canvas
        self.figure.subplots_adjust(bottom=0.25)
        self.canvas.draw()
    
    # Evenement qui actualise les valeures de la combobox quand on sélectionne une valeure
    def __on_combobox_changed(self) -> None:
        selected_text = self.list_ville.currentText()

        match selected_text:
            case "Région" | "Département" | "Commune":
                values = ["Retour"]
                values.extend(self.api.locality_names[f"{selected_text.replace("é", "e")}s"])
                self.dataname = f"{selected_text}s"
                self.list_ville.currentIndexChanged.disconnect(self.__on_combobox_changed)
                self.list_ville.clear()
                self.list_ville.addItems(values)
                self.list_ville.setCurrentIndex(1)
                self.graphic_button.setEnabled(True)
                self.list_ville.currentIndexChanged.connect(self.__on_combobox_changed)
            case "Retour":
                self.list_ville.clear()
                self.list_ville.addItems(["Choisissez le type de localité", "Commune", "Région", "Département"])
                self.graphic_button.setEnabled(False)
