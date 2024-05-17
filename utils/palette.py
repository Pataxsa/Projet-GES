"""
Module palette qui permet de changer la base des couleurs de l'interface
"""

from PySide6.QtGui import QPalette, QColor

class Palette(QPalette):
    """
    Classe Palette qui permet de générer une palette de couleur customisée
    """

    def __init__(self):
        super().__init__()

        colorsnormal = [
            QColor("#ffffff"), # Couleur labels
            QColor("#3c3c3c"), # Couleur boutons
            QColor("#787878"), # Couleur light
            QColor("#1e1e1e"), # Couleur dark
            QColor("#282828"), # Couleur mid
            QColor("#ffffff"), # Couleur du texte
            QColor("#99ebff"), # Couleur du texte éclairé
            QColor("#2d2d2d"), # Couleur de la base
            QColor("#1e1e1e") # Couleur du background
        ]

        colorsdisabled = [
            QColor("#9d9d9d"), # Couleur labels
            QColor("#2e2e2e"), # Couleur boutons
            QColor("#787878"), # Couleur light
            QColor("#1e1e1e"), # Couleur dark
            QColor("#282828"), # Couleur mid
            QColor("#545454"), # Couleur du texte
            QColor("#99ebff"), # Couleur du texte éclairé
            QColor("#1e1e1e"), # Couleur de la base
            QColor("#1e1e1e") # Couleur du background
        ]

        colorsall = [
            QColor("#ffffdc"), # Couleur labels
            QColor("#000000"), # Couleur boutons
            QColor("#000000"), # Couleur light
            QColor("#000000"), # Couleur dark
            QColor("#ffffff"), # Couleur mid
            QColor("#787878"), # Couleur du texte
            QColor("#5a5a5a"), # Couleur du texte éclairé
            QColor("#282828"), # Couleur de la base
            QColor("#000000") # Couleur du background
        ]

        self.setColorGroup(QPalette.ColorGroup.All, *colorsall)
        self.setColorGroup(QPalette.ColorGroup.Active, *colorsnormal)
        self.setColorGroup(QPalette.ColorGroup.Inactive, *colorsnormal)
        self.setColorGroup(QPalette.ColorGroup.Disabled, *colorsdisabled)
        self.setColorGroup(QPalette.ColorGroup.Normal, *colorsnormal)
