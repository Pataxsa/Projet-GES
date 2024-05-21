"""
Composant bouton sidebar

Module :
    PySide6.QtWidgets.QPushButton :
    PySide6.QtWidgets.QWidget : Classe de base des objets QtWidgets (méthodes et variables)
    PySide6.QtGui.QColor : Classe pour les couleurs
    PySide6.QtGui.QFont : Classe pour l'écriture (police) de Qt 
    PySide6.QtGui.QMovie : Pour que les gifs soient "mobile"
    PySide6.QtGui.QPixmap :
    PySide6.QtGui.QIcon : Pour avoir les images mouvantes (gif)
    PySide6.QtCore.Qt : Pour les fonctions spécifiques à Qt
    PySide6.QtCore.QVariantAnimation :
    PySide6.QtCore.QSize :
"""

from PySide6.QtWidgets import QPushButton, QWidget
from PySide6.QtGui import QColor, QFont, QMovie, QPixmap, QIcon
from PySide6.QtCore import Qt, QVariantAnimation, QSize

class SideButton(QPushButton):
    """
    Classe SideButton pour générer un bouton pour la sidebar
    """

    def __init__(self, icon: QPixmap, parent: QWidget = None, text: str = None, animduration: int = 700, bgcolor: str = "#3d3d3d", bgcolorhover: str = "#ff9000", bgcolorselected: str = "#3498db", font: str = "Arial", fontsize: int = 11, selected: bool = False) -> None:
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
    
    def __updateStyle(self, bgcolor: QColor) -> None:
        """
        Fonction pour mettre à jour le style

        Paramètres :
            > bgcolor (QColor) : couleur à mettre à jour
        
        Return : None
        """
        self.setStyleSheet(f"background-color: {bgcolor.name()}; color: white; border: solid 0px; border-radius: 7px; padding: 10px;")

    def setSelected(self, selected: bool) -> None:
        """
        Fonction setSelected qui permet de changer l'état de selection sur le bouton

        Paramètres :
            > selected (bool) : Booléen si le bouton est sélectionné ou non

        Return : None
        """
        
        self.currentbgcolor = (self.bgcolorselected if selected else self.bgcolor)
        self.__updateStyle(QColor(self.currentbgcolor))
        self.hoveranim.setEndValue(QColor(self.currentbgcolor))
    
    def __on_changed_frame(self) -> None:
        """
         Evenement lorsque l'on change de frame sur le gif
         
         Return : None
         """
        
        self.setIcon(QIcon(self.gif_icon.currentPixmap()))

        # Stopper à la dernière frame
        if self.gif_icon.currentFrameNumber() == self.gif_icon.frameCount()-1:
            self.gif_icon.stop()

    def enterEvent(self, event) -> None:
        """
        Evenement lorsque l'on passe sur le bouton (hover)
         
        Return : None
        """
        self.hoveranim.stop()
        self.hoveranim.start()
        self.gif_icon.stop()
        self.gif_icon.start()
        event.accept()
    
    def leaveEvent(self, event) -> None:
        """
         Evenement lorsque l'on quitte le bouton (inverse hover)
         
         Return : None
         """
        
        # Arrêt de l'animation et rembobinage à la frame 0
        self.gif_icon.stop()
        self.gif_icon.jumpToFrame(0)
        event.accept()
