import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QMessageBox, QComboBox,QSizePolicy
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QPalette
from PySide6.QtWebEngineWidgets import QWebEngineView
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from requests.exceptions import HTTPError
from utils.api import Api
from utils.map import MAP
from utils.local_serveur import LocalServer

class GUI(QMainWindow):
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
        self.map_button.clicked.connect(self.__showMap)


        # Créer le FigureCanvas pour afficher le graphique
        self.figure = Figure()
        self.figure.set_facecolor(central_widget.palette().color(QPalette.ColorRole.Window).name()) # Mettre le fond du canvas a la même couleur que le fond du menu
        self.canvas: FigureCanvas = FigureCanvas(self.figure)
        central_layout.addWidget(self.canvas)
        self.canvas.setMaximumSize(1000, 800) # Taille max du canvas
        self.canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding) # Fait en sorte que le canvas puisse s'étendre
        
        
        self.local_server = LocalServer(directory=".")

    def init(titre):
        app = QApplication(sys.argv)
        window = GUI(title = titre)
        window.show()
        sys.exit(app.exec_())

    def on_main_combo_box_changed(self):
        
        selected_text = self.list_ville.currentText()

        match selected_text:
            case "Région" | "Département" | "Commune":
                values = ["Retour"]
                values.extend(getattr(self.api, f"{selected_text.lower().replace("é", "e")}s"))
                self.dataname = f"{selected_text}s"
                self.list_ville.currentIndexChanged.disconnect(self.on_main_combo_box_changed)
                self.list_ville.clear()
                self.list_ville.addItems(values)
                self.list_ville.setCurrentIndex(1)
                self.list_ville.currentIndexChanged.connect(self.on_main_combo_box_changed)
            case "Retour":
                self.list_ville.clear()
                self.list_ville.addItems(["Choisissez le type de localité", "Commune", "Région", "Département"])


    def __showMap(self):
        if isinstance(self.centralWidget(), QWebEngineView):
            # Supprimer le widget central actuel s'il s'agit d'un WebEngineView
            web_view = self.centralWidget()
            layout = self.centralWidget().layout()
            layout.removeWidget(web_view)
            web_view.deleteLater()

        self.canvas.hide()
        # Démarrer le serveur local pour afficher la carte
        self.local_server.start_server()

        # Charger la carte dans le navigateur Web local
        self.web_view = QWebEngineView()
        self.web_view.load(QUrl("http://localhost:8000/../map.html"))

        # Remplacer le widget central actuel par la carte
        self.centralWidget().layout().addWidget(self.web_view)


    def __show_graphic(self):
        if isinstance(self.centralWidget(), QWebEngineView):
            # Supprimer le widget central actuel s'il s'agit d'un WebEngineView
            self.centralWidget().layout().deleteLater()

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

                # Réafficher le canvas maintenant que le graphique est prêt
                self.canvas.show()
        except HTTPError as e:
            error_message = f"Erreur de requête vers l'API: {str(e.response)}"
            QMessageBox.critical(None, "Erreur", error_message)
    
    def closeEvent(self, event):
        # Arrêter le serveur local lorsque la fenêtre est fermée
        self.local_server.stop_server()
        event.accept()