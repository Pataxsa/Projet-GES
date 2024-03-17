from utils.libs import checkLibs
checkLibs()
from utils.gui import Gui

gui = Gui("Recherche GES par Ville", False)

#Effectue un test de l'initialisation
gui.testinit()