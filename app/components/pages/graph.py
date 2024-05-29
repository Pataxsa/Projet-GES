"""
Page graph

Modules :
    PySide6.QtCore.Qt : Pour les fonctions spécifiques à Qt
    PySide6.QtGui.QPalette : Pour la palette de couleur des widgets
    PySide6.QtWidgets.QWidget : Classe de base des objets QtWidgets (méthodes et variables)
    PySide6.QtWidgets.QVBoxLayout : Pour mettre les éléments de manière vertical (les uns au-dessus des autres)
    PySide6.QtWidgets.QComboBox : Pour les boutons défilants
    PySide6.QtWidgets.QSizePolicy : Pour le dimensionement horizontal et vertical des widgets

    Api : Importe la classe Api    
"""

from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas,NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from PySide6.QtWidgets import QWidget, QVBoxLayout, QComboBox, QSizePolicy

from utils import Api

class GraphPage(QWidget):
    """
    Classe GraphPage pour générer la page graph
    """

    def __init__(self, api: Api, default_plot: int = 0, parent: QWidget = None) -> None:
        super().__init__(parent)

        # Api
        self.api = api

        # Données supplémentaires
        self.data_type = None
        self.type_plot = default_plot

        # Layout principal
        central_layout = QVBoxLayout()
        central_layout.setContentsMargins(0, 0, 0, 0)
        central_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.setLayout(central_layout)

        # Créer une combobox principale
        self.list_ville = QComboBox(self)
        self.list_ville.items = ["Choisissez le type de localité", "Commune", "Département", "Région"]
        self.list_ville.addItems(self.list_ville.items)
        self.list_ville.setFixedSize(200, 30)
        self.list_ville.currentIndexChanged.connect(self.__on_liste_ville_changed)
        central_layout.addSpacing(40)
        central_layout.addWidget(self.list_ville, alignment=Qt.AlignmentFlag.AlignHCenter)

        # Créer une combobox pour sélectionner le tracé du graphique
        self.list_type_plots = QComboBox(self)
        self.list_type_plots.items = ["Choisissez le type du tracé", "graphique à barres (défaut)", "figure remplie", "nuage de points", "tiges", "ligne droite"]
        self.list_type_plots.setFixedSize(200, 30)
        self.list_type_plots.addItems(self.list_type_plots.items)
        self.list_type_plots.currentIndexChanged.connect(self.__on_list_type_plots_changed)
        central_layout.addWidget(self.list_type_plots, alignment=Qt.AlignmentFlag.AlignHCenter)

        # Créer le FigureCanvas pour afficher le graphique
        self.figure = Figure()
        self.figure.set_facecolor(self.palette().color(QPalette.ColorRole.Window).name())
        self.figure.subplots_adjust(bottom=0.25)
        self.axe = self.figure.subplots()
        self.canvas = None

        # Liste des plots disponible
        self.plots = [self.axe.bar, self.axe.fill, self.axe.scatter, self.axe.stem, self.axe.plot]

    def __show_graphic(self) -> None:
        """
        Fonction qui affiche le graphique

        Return : None
        """

        # Créer le canva s'il n'est pas déjà créé
        if not self.canvas:
            self.canvas = FigureCanvas(self.figure)
            self.canvas.setMaximumSize(1000, 800)
            self.canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            menu = NavigationToolbar(self.canvas, self)
            
            self.layout().addWidget(menu, alignment=Qt.AlignmentFlag.AlignHCenter)
            self.layout().addWidget(self.canvas)

        # Donne les données au graphique
        inputdata = self.list_ville.currentText()
        data = self.api.getCO2(self.data_type, inputdata)
        dates = list(data.keys())
        totalco2 = list(data.values())

        # Effacer le contenu précédent du graphique
        self.axe.cla()
        
        # Créer le graphique
        self.plots[self.type_plot](dates, totalco2, label="CO2")
        self.axe.set_title(f"Bilan GES, {self.data_type[0:-1]} : {inputdata}", color="white")
        self.axe.set_xlabel('Dates',  color="white")
        self.axe.set_ylabel('Tonnes de CO2',  color="white")
        self.axe.legend()
        self.axe.tick_params(axis='x', rotation=90)
        self.axe.tick_params(labelcolor='white')

        # Mettre à jour le graphique dans le canva
        self.canvas.draw()
    
    def __on_liste_ville_changed(self) -> None:
        """
        Evenement qui actualise les valeurs de la combobox list_ville quand on sélectionne une valeur

        Return : None
        """

        selected_text = self.list_ville.currentText()

        match selected_text:
            case "Région" | "Département" | "Commune":
                values = ["Retour"]
                values.extend(self.api.locality_names[f"{selected_text.replace("é", "e")}s"])
                self.data_type = f"{selected_text}s"
                self.list_ville.currentIndexChanged.disconnect(self.__on_liste_ville_changed)
                self.list_ville.clear()
                self.list_ville.addItems(values)
                self.list_ville.currentIndexChanged.connect(self.__on_liste_ville_changed)
                self.list_ville.setCurrentIndex(1)
            case "Retour":
                self.list_ville.currentIndexChanged.disconnect(self.__on_liste_ville_changed)
                self.list_ville.clear()
                self.list_ville.addItems(self.list_ville.items)
                self.list_ville.currentIndexChanged.connect(self.__on_liste_ville_changed)
            case _:
                self.__show_graphic()

    def __on_list_type_plots_changed(self):
        """
        Evenement qui modifie le type du graphique quand on le choisit dans la combobox

        Return : None
        """

        selected_index = self.list_type_plots.currentIndex()-1
        selected_text_liste_ville = self.list_ville.currentText()

        if selected_index >= 0:
            self.type_plot = selected_index

            if self.canvas and selected_text_liste_ville not in self.list_ville.items:
                self.__show_graphic()
