"""
Composant bouton sidebar
"""

#TODO: ajouter icones (svg si statique ou gif si animé)

from PySide6.QtWidgets import QPushButton, QWidget
from PySide6.QtGui import QColor, QFont
from PySide6.QtCore import Qt, QVariantAnimation

class SideButton(QPushButton):
    """
    Classe SideButton pour générer un bouton pour la sidebar
    """

    def __init__(self, parent: QWidget = None, text: str = None, animduration: int = 500, bgcolor: str = "#3d3d3d", bgcolorhover: str = "#ff9000", bgcolorselected: str = "#3498db", font: str = "Arial", fontsize: int = 11, selected: bool = False) -> None:
        super().__init__(parent)

        # Données
        self.bgcolor = bgcolor
        self.bgcolorselected = bgcolorselected
        self.currentbgcolor = (bgcolorselected if selected else bgcolor)

        # Mettre les styles par défaut
        self.__updateStyle(bgcolor=QColor(self.currentbgcolor))
        self.setFont(QFont(font, fontsize))
        self.setFixedHeight(50)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setText(text)

        # Initialiser l'animation hover (couleur)
        self.hoveranim = QVariantAnimation(self)
        self.hoveranim.setDuration(animduration)
        self.hoveranim.setStartValue(QColor(bgcolorhover))
        self.hoveranim.setEndValue(QColor(self.currentbgcolor))
        self.hoveranim.valueChanged.connect(self.__updateStyle)
    
    # Mettre a jour le style
    def __updateStyle(self, bgcolor: QColor) -> None:
        self.setStyleSheet(f"background-color: {bgcolor.name()}; color: white; border: solid 0px; border-radius: 7px; padding: 10px;")

    def setSelected(self, selected: bool) -> None:
        """
        Fonction setSelected qui permet de changer l'état de selection sur le bouton
        """
        
        self.currentbgcolor = (self.bgcolorselected if selected else self.bgcolor)
        self.__updateStyle(QColor(self.currentbgcolor))
        self.hoveranim.setEndValue(QColor(self.currentbgcolor))

    # Evenement lorsque l'on passe sur le bouton (hover)
    def enterEvent(self, event) -> None:
        self.hoveranim.stop()
        self.hoveranim.start()
        event.accept()
    