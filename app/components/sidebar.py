"""
Composant sidebar
"""

from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPainter, QLinearGradient, QColor, QFont
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QStackedWidget

from app.components.sidebutton import SideButton
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
            SideButton(parent=self, text="Home", icon=f"{RESOURCE_PATH}\\icons\\home_button.gif", selected=True),
            SideButton(parent=self, text="Graph", icon=f"{RESOURCE_PATH}\\icons\\graph_button.gif"),
            SideButton(parent=self, text="Map", icon=f"{RESOURCE_PATH}\\icons\\map_button.gif")
        ]

        for index, button in enumerate(self.buttons):
            button.clicked.connect(lambda _, index=index: self.__changePage(index))
            central_layout.addSpacing(20)
            central_layout.addWidget(button)

    # Fonction pour changer de page
    def __changePage(self, index: int) -> None:
        clicked_button = self.buttons[index]
        
        for button in self.buttons:
            if button is clicked_button:
                button.setSelected(True)
            else:
                button.setSelected(False)
        
        self.page_manager.setCurrentIndex(index)

    # Changer le background de la barre (evenement)
    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        gradient = QLinearGradient(QPointF(0, 0), QPointF(self.width(), self.height()))

        for pos, color in enumerate(self.bgcolor):
            gradient.setColorAt(pos, QColor(color))
        painter.fillRect(self.rect(), gradient)

        event.accept()