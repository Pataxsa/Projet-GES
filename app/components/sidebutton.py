"""
Composant bouton sidebar
"""

from PySide6.QtWidgets import QPushButton, QWidget
from PySide6.QtGui import QColor, QFont, QMovie, QPixmap, QIcon
from PySide6.QtCore import Qt, QVariantAnimation, QSize

class SideButton(QPushButton):
    """
    Classe SideButton pour générer un bouton pour la sidebar
    """

    def __init__(self, icon: QPixmap, parent: QWidget = None, text: str = None, animduration: int = 500, bgcolor: str = "#3d3d3d", bgcolorhover: str = "#ff9000", bgcolorselected: str = "#3498db", font: str = "Arial", fontsize: int = 11, selected: bool = False) -> None:
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
        self.setIcon(QIcon(icon))
        self.setIconSize(QSize(25, 25))
        self.setText(f" {text}")

        # Icone du bouton
        self.gif_icon = QMovie(icon)
        self.gif_icon.setCacheMode(self.gif_icon.CacheMode.CacheAll)
        self.gif_icon.frameChanged.connect(self.__on_changed_frame)

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
    
    # Evenement lorsque l'on change de frame sur le gif
    def __on_changed_frame(self) -> None:
        self.setIcon(QIcon(self.gif_icon.currentPixmap()))

        if self.gif_icon.currentFrameNumber() == self.gif_icon.frameCount()-1:
            self.gif_icon.stop()

    # Evenement lorsque l'on passe sur le bouton (hover)
    def enterEvent(self, event) -> None:
        self.hoveranim.stop()
        self.hoveranim.start()
        self.gif_icon.stop()
        self.gif_icon.start()
        event.accept()
    
    # Evenement lorsque l'on quitte le bouton (inverse hover)
    def leaveEvent(self, event) -> None:
        self.gif_icon.stop()
        self.gif_icon.jumpToFrame(0)
        event.accept()
