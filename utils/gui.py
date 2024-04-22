"""
Module gui pour créer une interface
"""

# WARNING: LES IMPORTATIONS RALENTISSENT L'APP IL FAUT TOUJOURS OPTIMISER LES IMPORTATIONS COMME ICI (le preload doit se faire avant un maximum d'importations !)
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from os.path import isfile
from os import remove
from requests.exceptions import HTTPError
from utils.api import Api
from utils.map import MAP
from PIL import Image, ImageQt

class Gui(QMainWindow):
    """
    Classe Gui qui génère une interface
    Doc customtkinter: https://customtkinter.tomschimansky.com/documentation/
    """

    # Initialisation de la classe et des fenetres avec ses composants
    def __init__(self, title: str = "Title", resizable: bool = True, tests: bool = False) -> None:
        super().__init__()

        # Initialisation de l'API
        try:
            self.api = Api()
        except HTTPError as e:
            if tests:
                raise e
            # Afficher une erreur en cas d'échec de l'initialisation de l'API
            print("Erreur de requete vers l'API:", str(e.response))

        # Initialisation de la carte
        self.map = MAP(self.api)

        # Paramètres de l'interface
        self.title = title
        self.resizable = resizable
        self.minsize = (400, 200)
        self.tests = tests

        # Paramètres de l'API
        self.data_type = "Communes"

        # Appeler la méthode pour configurer l'interface
        self.init()

    def init(self) -> None:
        """
        Fonction init pour lancer une interface
        """

        # Supprimer la carte si elle existe (afin de la réactualiser par la suite)
        if isfile("map.html"):
            remove("map.html")

        self.setWindowTitle(self.title)
        self.setMinimumSize(*self.minsize)
        self.resize(800, 600)  # Taille par défaut de la fenêtre

        # Créer un widget central et un layout vertical
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        # Créer les widgets nécessaires
        self.list_ville = QComboBox()
        self.list_ville.addItems(["Régions", "Départements", "Communes"])
        self.list_ville.currentIndexChanged.connect(self.__on_selected)

        self.ville_label = QLabel("Type de localité : ")

        self.graphic_button = QPushButton("Générer un graphique")
        self.graphic_button.setEnabled(False)
        self.graphic_button.clicked.connect(self.__show_graphic)

        self.map_button = QPushButton("Générer une carte")
        self.map_button.clicked.connect(self.__generatemap)

        # Charger l'image de fond
        img_path = f"{self.api.basepath}\\interface\\img\\GES.jpg"
        self.img = Image.open(img_path)
        self.background_photo = QLabel()
        self.set_background_image()
        self.__on_resize()

        # Ajouter les widgets au layout vertical
        layout.addWidget(self.ville_label)
        layout.addWidget(self.list_ville)
        layout.addWidget(self.graphic_button)
        layout.addWidget(self.map_button)
        layout.addWidget(self.background_photo)

        # Définir le widget central de la fenêtre principale
        self.setCentralWidget(central_widget)
    
    def set_background_image(self):
        # Charger l'image et la redimensionner pour s'adapter à la taille du QLabel
        img_path = f"{self.api.basepath}\\interface\\img\\GES.jpg"
        img = Image.open(img_path)

        # Redimensionner l'image pour s'adapter à la taille du QLabel
        label_size = self.background_photo.size()
        img_resized = img.resize(label_size, Image.ANTIALIAS)

        # Convertir l'image PIL redimensionnée en QImage
        qimage = ImageQt.ImageQt(img_resized)

        # Convertir le QImage en QPixmap
        pixmap = QPixmap.fromImage(qimage)

        # Afficher le QPixmap dans le QLabel
        self.background_photo.setPixmap(pixmap)

    def close(self) -> None:
        """
        Fonction close pour fermer l'interface
        """

        self.window.destroy()

    # Fonction privé qui permet d'afficher le graphique sur l'interface
    def __show_graphic(self):
        # Méthode pour afficher un graphique
        try:
            inputdata = self.list_ville.currentText()
            data = self.api.getCO2(self.data_type, inputdata)
            dates = list(data.keys())
            totalco2 = list(data.values())

            # Effacer le graphique précédent
            self.figure.clear()

            ax = self.figure.add_subplot(111)
            ax.bar(dates, totalco2, label="CO2")
            ax.set_title(f"Bilan GES {self.data_type.removesuffix('s')} {inputdata}")
            ax.set_xlabel('Dates')
            ax.set_ylabel('Tonnes de CO2')
            ax.set_xticklabels(dates, rotation=90)
            ax.legend()

            self.graphic_canvas.draw()

        except HTTPError as e:
            if self.tests:
                raise e
            print("Erreur de requete vers l'API:", str(e.response))

    # Fonction privé pour générer une carte en fonction du CO2
    def __generatemap(self, save: bool = True) -> None:
        if save:
            self.map.save("map.html")

    # Fonction privé (evenement) qui ajuste la position de la barre de selection/change le texte du label en fonction de la valeure sélectionnée
    def __on_selected(self, index):
        selected_option = self.list_ville.currentText()

        if selected_option in ["Régions", "Départements", "Communes"]:
            self.data_type = selected_option
            self.graphic_button.setEnabled(True)
            self.ville_label.setText(f"{selected_option[:-1]} : ")

            # Charger les nouvelles options en fonction de la sélection
            if selected_option == "Régions":
                new_options = ["Retour"] + self.api.regions
            elif selected_option == "Départements":
                new_options = ["Retour"] + self.api.departements
            elif selected_option == "Communes":
                new_options = ["Retour"] + self.api.communes

            self.list_ville.clear()
            self.list_ville.addItems(new_options)
            self.list_ville.setCurrentIndex(1)  # Sélectionner le premier élément par défaut

        elif selected_option == "Retour":
            self.ville_label.setText("Type de localité : ")
            self.list_ville.clear()
            self.list_ville.addItems(["Régions", "Départements", "Communes"])
            self.list_ville.setCurrentIndex(0)
            self.graphic_button.setEnabled(False)

        text_length = len(self.ville_label.text())
        self.list_ville.setGeometry(text_length * 10, self.list_ville.y(), 150, 30)
    
    # Fonction privé (evenement) qui ajuste la taille du fond lorsque l'on redimentionne la taille de la fenetre
    def __on_resize(self, event) -> None:
        # Redimensionner l'image en fonction de la taille actuelle du QLabel
        img_resized = self.img.scaled(self.canvas.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        qimage = ImageQt(img_resized)
        
        pixmap = QPixmap.fromImage(qimage)
        self.canvas.setPixmap(pixmap)

    def resizeEvent(self, event):
        super().resizeEvent(event)
