"""
Page graph
"""

from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas,NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QComboBox, QSizePolicy

from utils.api import Api

class GraphPage(QWidget):
    """
    Classe GraphPage pour générer la page graph
    """

    def __init__(self, api: Api, parent: QWidget = None) -> None:
        super().__init__(parent)

        # Api
        self.api = api

        # Données supplémentaires
        self.dataname = None

        # Layout principal
        central_layout = QVBoxLayout()
        central_layout.setContentsMargins(0, 0, 0, 0)
        central_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.setLayout(central_layout)

        # Créer une combobox principale
        self.list_ville = QComboBox(self)
        self.list_ville.addItems(["Choisissez le type de localité", "Commune", "Région", "Département"])
        self.list_ville.setStyleSheet(" QComboBox { width: 200px;  } ")  # Définir une largeur minimale
        self.list_ville.currentIndexChanged.connect(self.__on_combobox_changed)
        central_layout.addSpacing(40)
        central_layout.addWidget(self.list_ville, alignment=Qt.AlignmentFlag.AlignHCenter)  # Centrer la combobox horizontalement

        # Bouton pour gen le graph
        self.graphic_button = QPushButton("Générer un graphique", self)
        self.graphic_button.setEnabled(False)
        self.graphic_button.setFixedSize(150, 30)
        self.graphic_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.graphic_button.clicked.connect(self.__show_graphic)
        central_layout.addWidget(self.graphic_button, alignment=Qt.AlignmentFlag.AlignHCenter)

        # Créer le FigureCanvas pour afficher le graphique
        self.figure = Figure()
        self.figure.set_facecolor(self.palette().color(QPalette.ColorRole.Window).name())
        self.figure.subplots_adjust(bottom=0.25)
        self.axe = self.figure.subplots()
        self.canvas = None

    # Affiche le graphique
    def __show_graphic(self) -> None:
        if not self.canvas:
            self.canvas = FigureCanvas(self.figure)
            self.canvas.setMaximumSize(1000, 800)
            self.canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            menu = NavigationToolbar(self.canvas,self)
            
            self.layout().addWidget(menu,alignment=Qt.AlignmentFlag.AlignHCenter)
            self.layout().addWidget(self.canvas)
        inputdata = self.list_ville.currentText()
        data = self.api.getCO2(self.dataname, inputdata)
        dates = list(data.keys())
        totalco2 = list(data.values())

        # Effacer le contenu précédent du graphique
        self.axe.cla()

        # Créer le graphique
        self.axe.bar(dates, totalco2, label="CO2")
        self.axe.set_title(f"Bilan GES, {self.dataname[0:-1]} : {inputdata}", color="white")
        self.axe.set_xlabel('Dates',  color="white")
        self.axe.set_ylabel('Tonnes de CO2',  color="white")
        self.axe.legend()
        self.axe.tick_params(axis='x', rotation=90)
        self.axe.tick_params(labelcolor='white')

        # Mettre à jour le graphique dans le canvas
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
