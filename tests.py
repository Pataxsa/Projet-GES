import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QMessageBox, QComboBox
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from os.path import isfile, join
from os import remove
from requests.exceptions import HTTPError
from utils.api import Api
from utils.map import MAP


class MainWindow(QMainWindow):
    def __init__(self, title: str = "Emissions de GES par types de localités", resizable: bool = True, tests: bool = False) -> None:
        super().__init__()
        self.setMinimumSize(800, 600)
        self.setWindowTitle(title)

        self.api = Api()
        self.map = MAP(self.api)
        self.dataname = "Communes"

        # Créer un widget central pour la fenêtre
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Créer un layout vertical pour le widget central
        central_layout = QVBoxLayout(central_widget)
        central_layout.setContentsMargins(20, 20, 20, 20)
        central_layout.setAlignment(Qt.AlignTop)

        # Créer une combobox principale
        self.list_ville = QComboBox()
        self.list_ville.setGeometry(len(self.list_ville.currentText()) + 5,30,30,30)
        self.list_ville.addItems(["===========","Commune", "Région", "Département","==========="])

        # Appliquer le style pour centrer le texte dans la ComboBox
        self.list_ville.setStyleSheet("QComboBox::item { text-align: center; }")
        central_layout.addWidget(self.list_ville)

        # Connecter le signal de changement de sélection de la combobox principale
        self.ignore_main_combo_box_change = False
        self.list_ville.currentIndexChanged.connect(self.on_main_combo_box_changed)

        # Créer un layout horizontal pour les boutons
        button_layout = QHBoxLayout()
        central_layout.addLayout(button_layout)

        research_button = QPushButton("Générer un graphique")
        map_button = QPushButton("Afficher une carte")

        # Ajouter les boutons au layout horizontal
        button_layout.addWidget(research_button)
        button_layout.addWidget(map_button)

        research_button.setFixedSize(150, 30)
        map_button.setFixedSize(150, 30)

        # Associer les fonctions aux boutons
        research_button.clicked.connect(self.__show_graphic)
        map_button.clicked.connect(self.__generatemap)

        # Créer le FigureCanvas pour afficher le graphique
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        central_layout.addWidget(self.canvas)

        central_layout.addStretch(1)

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
            self.list_ville.addItems(["Commune", "Région", "Département"])
            self.list_ville.setCurrentIndex(0)
        
        self.list_ville.setCurrentText(selected_text)
        self.ignore_main_combo_box_change = False

    def init():
        if isfile("map.html"):
            remove("map.html")

        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())

    def __generatemap(self):
        self.map.save("map.html")

    def __show_graphic(self):
        try:
            if not self.list_ville.currentText() in ["Retour","Commune", "Région", "Département"]:
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
                ax.set_title(f"Bilan GES {self.dataname[0:-1]} : {inputdata}")
                ax.set_xlabel('Dates')
                ax.set_ylabel('Tonnes de CO2')
                ax.legend()
                ax.tick_params(axis='x', rotation=90)

                # Mettre à jour le graphique dans le canvas
                self.canvas.draw()

        except HTTPError as e:
            error_message = f"Erreur de requête vers l'API: {str(e.response)}"
            QMessageBox.critical(None, "Erreur", error_message)




MainWindow.init()