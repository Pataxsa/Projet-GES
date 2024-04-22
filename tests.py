"""
Module tests pour tester l'interface
"""

import sys
from PyQt5.QtWidgets import QApplication
from utils.gui import Gui


def test():

    #Effectue un test de l'initialisation
    app = QApplication(sys.argv)
    gui = Gui("Affichage du GES par types de localités")
    gui.init()
    sys.exit(app.exec_())

test()

