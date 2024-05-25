"""
Composant sidebar

Module :
    PySide6.QtCore.Qt : Pour les fonctions spécifiques à Qt
    PySide6.QtCore.QPointF : Pour cibler un point de l'élément (pour le dégradé)
    PySide6.QtGui.QPainter : Pour dessiner et ajouter les couleurs aux éléments
    PySide6.QtGui.QLinearGradient : Pour faire un dégradé de couleurs
    PySide6.QtGui.QColor : Classe pour les couleurs de Qt
    PySide6.QtGui.QFont : Classe pour l'écriture (police) de Qt
    PySide6.QtWidgets.QWidget : Classe de base des objets QtWidgets (méthodes et variables)
    PySide6.QtWidgets.QVBoxLayout : Pour mettre les éléments de manière vertical (les uns au-dessus des autres)
    PySide6.QtWidgets.QLabel : Pour gérer l'affichage, le placement et la taille des éléments sur la page
    PySide6.QtWidgets.QStackedWidget : Widget pour superposer les widgets
    
    SideButton : Import les boutons à ajouter à la sidebar
    RESOURCE_PATH : Chemin d'accès aux ressources
"""

from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPainter, QLinearGradient, QColor, QFont
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QStackedWidget

from app.components import SideButton
from utils.constants import RESOURCE_PATH

class SideBar(QWidget):
    """
    Classe SideBar pour générer la sidebar
    """

    def __init__(self, page_manager: QStackedWidget, labeltext: str = "Projet-GES", bgcolor: list[str] = ["#051c2a", "#44315f"], parent: QWidget = None) -> None:
        super().__init__(parent)

        # Données
        self.bgcolor = bgcolor
        
        # Widget pour gérer les pages
        self.page_manager = page_manager

        # Layout principal
        central_layout = QVBoxLayout()
        central_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(central_layout)

        central_layout.addSpacing(20)

        # Label
        label = QLabel(self)
        label.setText(labeltext)
        label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        central_layout.addWidget(label)

        # Boutons
        self.buttons = [
            SideButton(parent=self, text="Accueil", icon=f"{RESOURCE_PATH}\\icons\\home_button.gif", selected=True),
            SideButton(parent=self, text="Graphique", icon=f"{RESOURCE_PATH}\\icons\\graph_button.gif"),
            SideButton(parent=self, text="Carte", icon=f"{RESOURCE_PATH}\\icons\\map_button.gif")
        ]

        # Ajout d'évènement, d'index et définition d'espacements aux boutons
        for index, button in enumerate(self.buttons):
            button.clicked.connect(lambda _, index=index: self.__changePage(index))
            central_layout.addSpacing(20)
            central_layout.addWidget(button)

    def __changePage(self, index: int) -> None:
        """
        Fonction pour changer de page
        
        Paramètres :
            > index (int) : index de la page à afficher

        Return : None
        """

        clicked_button = self.buttons[index]
        
        for button in self.buttons:
            if button is clicked_button:
                button.setSelected(True)
            else:
                button.setSelected(False)
        
        self.page_manager.setCurrentIndex(index)

    def paintEvent(self, event) -> None:
        """
        Fonction pour changer le background de la sidebar (evenement)

        Return : None
        """
        
        painter = QPainter(self)
        gradient = QLinearGradient(QPointF(0, 0), QPointF(self.width(), self.height()))

        for pos, color in enumerate(self.bgcolor):
            gradient.setColorAt(pos, QColor(color))
        painter.fillRect(self.rect(), gradient)

        event.accept()