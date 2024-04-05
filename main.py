"""
Module main pour créer et lancer l'interface
"""

from utils.libs import checkLibs
# Vérifie si les dépendances sont installées (et les installes)
checkLibs()
from utils.gui import Gui

# Crée une interface
gui = Gui("Recherche GES par Lieux")
gui.init()
