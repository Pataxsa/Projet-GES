"""
Module main pour créer et lancer l'interface
"""
import subprocess
from utils.gui import Gui

chemin = "configuration\\install_poetry.sh"

try:
    subprocess.run(["bash", chemin], check=True)
    print("Poetry a été installé avec succès!")

except subprocess.CalledProcessError as e:
    print(f"Une erreur s'est produite lors de l'installation de Poetry : {e}")

#Crée une interface
gui = Gui("Recherche GES par Lieux")
gui.init()