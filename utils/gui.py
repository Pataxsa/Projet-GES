import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QMessageBox, QComboBox,QSizePolicy
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QPalette
from PySide6.QtWebEngineWidgets import QWebEngineView
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from os.path import isfile
from os import remove
from requests.exceptions import HTTPError
from utils.api import Api
from utils.map import MAP


class MainWindow(QMainWindow):
    def __init__(self, title: str = "Emissions de GES par types de localités") -> None:
        super().__init__()
        self.setWindowTitle(title)
        self.setMinimumSize(800,600) #pas de pb avec les redimensionnements

        self.api = Api()
        self.map = MAP(self.api)
        self.dataname = "Communes"

        # Créer un widget central pour la fenêtre
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Créer un layout vertical pour le widget central
        central_layout = QVBoxLayout(central_widget)
        central_layout.setContentsMargins(20, 20, 20, 20)
        central_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Centrer les éléments verticalement

        # Créer une combobox principale
        self.list_ville = QComboBox(self)
        self.list_ville.addItems(["Choisissez le type de localité","Commune", "Région", "Département"])
        self.list_ville.setStyleSheet("QComboBox { min-width: 200px; }")  # Définir une largeur minimale
        self.list_ville.currentIndexChanged.connect(self.on_main_combo_box_changed)

        central_layout.addWidget(self.list_ville, alignment=Qt.AlignmentFlag.AlignHCenter)  # Centrer la combobox horizontalement
        self.ignore_main_combo_box_change = False

        # Créer un layout horizontal pour les boutons
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        button_layout.setContentsMargins(0, 10, 0, 0)
        button_layout.setSpacing(20)
        central_layout.addLayout(button_layout)

        self.research_button = QPushButton("Générer un graphique", self)
        self.map_button = QPushButton("Afficher une carte", self)

        # Ajouter les boutons au layout horizontal
        button_layout.addWidget(self.research_button)
        button_layout.addWidget(self.map_button)

        self.research_button.setFixedSize(150, 30)
        self.map_button.setFixedSize(150, 30)

        # Associer les fonctions aux boutons
        self.research_button.clicked.connect(self.__show_graphic)
        self.map_button.clicked.connect(self.__generatemap)


        """ A faire, en cours de test
        self.web_view = QWebEngineView(self)
        central_layout.addWidget(self.web_view, alignment=Qt.AlignmentFlag.AlignCenter)
        """


        # Créer le FigureCanvas pour afficher le graphique
        self.figure = Figure()
        self.figure.set_facecolor(self.palette().color(QPalette.ColorGroup.Current, QPalette.ColorRole.Dark).name()) # Mettre le fond du canvas a la même couleur que le fond du menu
        self.canvas: FigureCanvas = FigureCanvas(self.figure)
        central_layout.addWidget(self.canvas)
        self.canvas.setMaximumSize(1000, 800) # Taille max du canvas
        self.canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding) # Fait en sorte que le canvas puisse s'étendre
    
    def init():
        if isfile("map.html"):
            remove("map.html")

        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec())

    def on_main_combo_box_changed(self):
        if self.ignore_main_combo_box_change:
            return
        
        selected_text = self.list_ville.currentText()
        self.ignore_main_combo_box_change = True

        if selected_text == "Commune":
            self.dataname = "Communes"
            self.list_ville.clear()
            self.list_ville.addItems(["Retour"] + self.api.communes)
            self.list_ville.setCurrentIndex(1)

        elif selected_text == "Région":
            self.dataname = "Régions"
            self.list_ville.clear()
            self.list_ville.addItems(["Retour"] + self.api.regions)
            self.list_ville.setCurrentIndex(1)

        elif selected_text == "Département":
            self.dataname = "Départements"
            self.list_ville.clear()
            self.list_ville.addItems(["Retour"] + self.api.departements)
            self.list_ville.setCurrentIndex(1)
            
        elif selected_text == "Retour":
            self.list_ville.clear()
            self.list_ville.addItems(["Choisissez le type de localité","Commune", "Région", "Département"])
            self.list_ville.setCurrentIndex(0)
        
        self.list_ville.setCurrentText(selected_text)
        self.ignore_main_combo_box_change = False


    def __generatemap(self):
        self.map.save("map.html")


    def __show_graphic(self):
        try:
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
        except HTTPError as e:
            error_message = f"Erreur de requête vers l'API: {str(e.response)}"
            QMessageBox.critical(None, "Erreur", error_message)


MainWindow.init()