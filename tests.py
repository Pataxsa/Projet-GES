"""
Module tests pour tester l'interface
"""

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QMessageBox, QComboBox
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Figure
from os.path import isfile
from os import remove
from requests.exceptions import HTTPError
from utils.api import Api
from utils.map import MAP
from PIL import Image

class MainWindow(QMainWindow):
    def __init__(self, title: str = "Title", resizable: bool = True, tests: bool = False) -> None:
        super().__init__()
        self.setMinimumSize(400, 200)
        self.setWindowTitle("Fenêtre avec deux boutons")

        self.api = Api()
        self.map = MAP(self.api)

        # Créer un widget central pour la fenêtre
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Créer un layout vertical pour le widget central
        central_layout = QVBoxLayout(central_widget)
        central_layout.setContentsMargins(20, 20, 20, 20)
        central_layout.setAlignment(Qt.AlignTop)

        # Créer une combobox principale
        self.list_ville = QComboBox()
        self.list_ville.addItems(["Commune", "Région", "Département"])
        central_layout.addWidget(self.list_ville)

        # Connecter le signal de changement de sélection de la combobox principale
        self.list_ville.currentIndexChanged.connect(self.on_main_combo_box_changed)

        # Créer un layout horizontal pour les boutons
        button_layout = QHBoxLayout()
        central_layout.addLayout(button_layout)

        # Créer les boutons
        research_button = QPushButton("Générer un graphique")
        map_button = QPushButton("Afficher une carte")

        # Ajouter les boutons au layout horizontal
        button_layout.addWidget(research_button)
        button_layout.addWidget(map_button)

        # Définir les politiques de taille des boutons pour qu'ils restent fixes
        research_button.setFixedSize(150, 30)
        map_button.setFixedSize(150, 30)

        # Associer les fonctions aux signaux des boutons
        research_button.clicked.connect(self.__show_graphic)
        map_button.clicked.connect(self.__generatemap)

        # Ajouter un étirement (stretch) au layout vertical
        central_layout.addStretch(1)

        # éviter les erreurs
        self.ignore_main_combo_box_change = False

    def on_main_combo_box_changed(self, index):
        if self.ignore_main_combo_box_change:
            return

        selected_text = self.list_ville.currentText()
        self.ignore_main_combo_box_change = True

        if selected_text == "Commune":
            self.list_ville.clear()
            self.list_ville.addItems(["Retour"] + self.api.communes)
        elif selected_text == "Région":
            self.list_ville.clear()
            self.list_ville.addItems(["Retour"] + self.api.regions)
        elif selected_text == "Département":
            self.list_ville.clear()
            self.list_ville.addItems(["Retour"] + self.api.departements)
        elif selected_text == "Retour":
            self.list_ville.clear()
            self.list_ville.addItems(["Commune", "Région", "Département"])
        self.list_ville.setCurrentIndex(1)

        self.ignore_main_combo_box_change = False

    def init():
        if isfile("map.html"):
            remove("map.html")

        app = QApplication(sys.argv)
        window = MainWindow()

        window.show()
        sys.exit(app.exec_())

    def __generatemap(self) -> None:
        self.map.save("map.html")

    def __show_graphic(self) -> None:
        try:
            inputdata = self.list_ville.get()
            data = self.api.getCO2(self.dataname, inputdata)
            dates = list(data.keys())
            totalco2 = list(data.values())

            self.canvas.delete("all") # supprimer l'image de fond

            fig, ax = plt.subplots(num="GES")
            ax.set_title(f"Bilan GES {self.dataname[:-1]} {inputdata}")
            ax.bar(dates, totalco2, label="CO2")

            plt.xlabel('Dates')
            plt.ylabel('Tonnes de CO2')

            plt.xticks(rotation=90) # dates à la verticale
            ax.legend()

            fig.set_figwidth(fig.get_figwidth() * 1.2)
            fig.set_figheight(fig.get_figheight() * 1.2)

            graphic = Figure(fig, master=self.window)

            if self.graphic_widget is not None:
                self.graphic_widget.destroy()

            self.graphic_widget = graphic.get_tk_widget()
            self.graphic_widget.place(relx=0.5, y=500, anchor="center")

            self.window.minsize(self.minsize[0] + 600, self.minsize[1] + 680)

            plt.close()
        except HTTPError as e:
            if self.tests: raise e
            QMessageBox.critical("Erreur", "Erreur de requete vers l'API: " + str(e.response))



MainWindow.init()

