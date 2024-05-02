"""
Composant messagebox
"""

from PySide6.QtWidgets import QMessageBox, QWidget
from PySide6.QtGui import QIcon

from utils.constants import RESOURCE_PATH

class MessageBox(QMessageBox):
    """
    Classe MessageBox pour générer une boite a message
    """

    # Initialisation (constructeur)
    def __init__(self) -> None:
        super().__init__()
    
    @staticmethod
    def show(parent: QWidget = None, window_icon: QIcon = QIcon(f"{RESOURCE_PATH}\\icons\\icon-x32.ico"), title: str = "python", icon: QMessageBox.Icon = QMessageBox.Icon.Critical, text: str = None, informative_text: str = None, detailed_text: str = None, buttons: QMessageBox.StandardButton = QMessageBox.StandardButton.Ok) -> None:
        """
        Fonction statique show qui permet l'affichage de la MessageBox
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