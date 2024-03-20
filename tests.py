"""Module tests pour tester l'interface"""

from utils.gui import Gui

def test():
    """
    Effectue un test de l'initialisation
    """

    gui = Gui("Recherche GES par Ville", tests=True)

    gui.testinit()
