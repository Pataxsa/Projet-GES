"""
Composant messagebox

Module :
    PySide6.QtWidgets.QMessageBox : Classe offrant des boites à message interactives
    PySide6.QtWidgets.QWidget : Classe de base des objets QtWidgets
    PySide6.QtGui.QIcon : Pour avoir des images mouvantes (gif)

    RESOURCE_PATH : Chemin d'accès aux ressources
"""

from PySide6.QtWidgets import QMessageBox, QWidget
from PySide6.QtGui import QIcon

from utils.constants import RESOURCE_PATH

class MessageBox(QMessageBox):
    """
    Classe MessageBox pour générer une boite à message
    """

    # Initialisation (constructeur)
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
    
    @staticmethod
    def show(parent: QWidget = None, window_icon: QIcon = QIcon(f"{RESOURCE_PATH}\\icons\\icon-x32.ico"), title: str = "python", icon: QMessageBox.Icon = QMessageBox.Icon.Critical, text: str = None, informative_text: str = None, detailed_text: str = None, buttons: QMessageBox.StandardButton = QMessageBox.StandardButton.Ok) -> None:
        """
        Fonction statique show qui permet l'affichage de la MessageBox

        Paramètres :
            > parent (QWidget) : Parent de la messagebox
            > window_icon (QIcon) : Icone qui va s'ajouter dans la messagebox
            > title (str) : Titre de la fenêtre de la boite à message
            > icon (QMessageBox.Icon) : Icone de la boite à message
            > text (str) : Texte de la boite à message
            > informative_text (str) : Texte supplémentaire bonus
            > detailed_text (str) : Texte détaillé bonus dans la messagebox
            > buttons (QMessageBox.StandardButton) : Bouton à afficher dans la boite à message

        Return : None
        """

        messagebox = QMessageBox()
        messagebox.setParent(parent)
        messagebox.setWindowTitle(title)
        if window_icon != None:
            messagebox.setWindowIcon(window_icon)
        messagebox.setIcon(icon)
        messagebox.setText(text)
        messagebox.setInformativeText(informative_text)
        messagebox.setDetailedText(detailed_text)
        messagebox.setStandardButtons(buttons)
        messagebox.exec()