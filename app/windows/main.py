from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QComboBox, QSizePolicy, QMenu, QHBoxLayout
from PySide6.QtCore import Qt, QUrl
import os,sys
from PySide6.QtMultimedia import QSoundEffect
from PySide6.QtGui import QPalette,QIcon
from PySide6.QtWebEngineCore import QWebEngineSettings
from PySide6.QtWebEngineWidgets import QWebEngineView
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from utils.api import Api
from utils.map import Map
from utils.constants import RESOURCE_PATH

class Main(QMainWindow):
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

        # Créer une combobox principale
        self.list_ville = QComboBox(self)
        self.list_ville.addItems(["Choisissez le type de localité","Commune", "Région", "Département"])
        self.list_ville.setStyleSheet("QComboBox { min-width: 200px; }")  # Définir une largeur minimale
        self.list_ville.currentIndexChanged.connect(self.on_main_combo_box_changed)

        self.central_layout.addWidget(self.list_ville, alignment=Qt.AlignmentFlag.AlignHCenter)  # Centrer la combobox horizontalement

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
        self.menu_button.setGeometry(0, 0, 100, 30)

        # Créer un layout horizontal pour les boutons du menu et de génération de graphiques
        button_layout = QHBoxLayout()

        # Ajouter un espace extensible à gauche
        button_layout.addStretch(1)

        # Créer un bouton pour générer des graphiques
        self.graphic_button = QPushButton("Générer le graphique", self)
        self.graphic_button.setFixedSize(150, 30)
        self.graphic_button.clicked.connect(self.__show_graphic)

        # Ajouter le bouton de génération de graphiques au layout horizontal
        button_layout.addWidget(self.graphic_button)

        # Créer un bouton pour enregistrer les graphiques
        self.save_button = QPushButton("Enregistrer le graphique", self)
        self.save_button.setFixedSize(150, 30)
        self.save_button.clicked.connect(self.save_graph)

        # Ajouter le bouton pour enregistrer les graphiques au layout horizontal
        button_layout.addWidget(self.save_button)

        # Aligner les éléments à droite
        button_layout.addStretch(1)

        # Ajouter le layout horizontal au layout vertical central
        self.central_layout.addLayout(button_layout)

        # Masquer le bouton jusqu'à ce qu'un graphique soit généré
        self.save_button.hide()

        # Créer le FigureCanvas pour afficher le graphique
        self.figure = Figure()
        self.figure.set_facecolor(central_widget.palette().color(QPalette.ColorRole.Window).name()) # Mettre le fond du canvas a la même couleur que le fond du menu
        self.canvas: FigureCanvas = FigureCanvas(self.figure)
        self.central_layout.addWidget(self.canvas)
        self.canvas.setMaximumSize(1000, 800) # Taille max du canvas
        self.canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding) # Fait en sorte que le canvas puisse s'étendre


        self.web_view = QWebEngineView()
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../map.html"))
        self.web_view.settings().setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        self.web_view.setZoomFactor(0.85)
        self.web_view.load(QUrl.fromLocalFile(file_path))

        # Ajouter la carte, masquée
        self.central_layout.addWidget(self.web_view)
        self.web_view.hide()
        self.list_ville.hide()
        self.graphic_button.hide()
    

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
        #cacher widgets pour faire des graphiques
        self.canvas.hide()
        self.list_ville.hide()
        self.graphic_button.hide()
        self.save_button.hide()
        self.web_view.show()

    def __show_graphic(self):
        self.web_view.hide()
        self.list_ville.show()
        self.graphic_button.show()
        self.canvas.show()
        if not self.list_ville.currentText() in ["Retour","Commune", "Région", "Département","Choisissez le type de localité"]:
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
            self.save_button.show()
        
    def play_sound(self):
        self.sound_effect = QSoundEffect()
        self.sound_effect.setSource(QUrl.fromLocalFile(f"{RESOURCE_PATH}\\sounds\\loading_sound.wav"))
        self.sound_effect.play()
