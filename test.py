from utils.libs import checkLibs
checkLibs()
from utils.gui import Gui

#Effectue un test de l'initialisation
def test():
    gui = Gui("Recherche GES par Ville", False)

    gui.testinit()