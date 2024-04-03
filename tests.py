"""Module tests pour tester l'interface"""

from utils.gui import Gui
from customtkinter import *

def test():
    """
    Effectue un test de l'initialisation
    """

    gui = Gui("Recherche GES par Ville", tests=True)
    gui.testinit()


#test pour remplacer tkinter par customtkinter