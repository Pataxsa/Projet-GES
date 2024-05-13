"""
Composant sidebar
"""

#TODO: modifier pour rendre plus clean

from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPalette, QPainter, QLinearGradient, QColor, QFont
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QStackedWidget

class SideBar(QWidget):
    """
    Classe SideBar pour générer la sidebar
    """

    def __init__(self, page_manager: QStackedWidget, parent: QWidget = None) -> None:
        super().__init__(parent)

        self.setAutoFillBackground(True)

        # Widget pour gérer les pages
        self.page_manager = page_manager

        # Layout principal
        central_layout = QVBoxLayout()
        central_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(central_layout)

        # Label
        label = QLabel(self)
        label.setText("Projet-GES")
        label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        central_layout.addWidget(label)

        # Ajout d'un espace entre les bouttons et le label
        central_layout.addSpacing(20)

        # Boutons
        self.buttons = [
            QPushButton(parent=self, text="Home"),
            QPushButton(parent=self, text="Graph"),
            QPushButton(parent=self, text="Map")
        ]
        self.selected_style = "background-color: #3498db; color: white; border: solid 0px; border-radius: 7px; padding: 10px;"
        self.other_style = "background-color: #3d3d3d; color: white; border: solid 0px; border-radius: 7px; padding: 10px;"


        for index, button in enumerate(self.buttons):
            if index == 0:
                button.setStyleSheet(self.selected_style)
            else:
                button.setStyleSheet(self.other_style)
            
            button.setFont(QFont("Arial", 10))
            button.clicked.connect(lambda _, index=index: self.__changePage(index))
            button.setFixedHeight(50)
            central_layout.addSpacing(20)
            central_layout.addWidget(button)

    # Fonction pour changer de page
    def __changePage(self, index: int) -> None:
        clicked_button = self.buttons[index]
        
        for button in self.buttons:
            if button is clicked_button:
                button.setStyleSheet(self.selected_style)
            else:
                button.setStyleSheet(self.other_style)
        
        self.page_manager.setCurrentIndex(index)

    # Changer le background de la barre
    def paintEvent(self, event):
        painter = QPainter(self)
        gradient = QLinearGradient(QPointF(0, 0), QPointF(self.width(), self.height()))
        gradient.setColorAt(0, QColor("#051c2a"))
        gradient.setColorAt(1, QColor("#44315f"))
        painter.fillRect(self.rect(), gradient)