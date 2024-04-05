"""
Module main pour créer et lancer l'interface
"""
import subprocess
from utils.gui import Gui

#Installation des modules nécessaires

"""
try:
    subprocess.run(["pip","install","poetry"])
    subprocess.run(["poetry","install"])

    print("Poetry a été installé avec succès!")

except subprocess.CalledProcessError as e:
    print(f"Une erreur s'est produite lors de l'installation de Poetry : {e}")
"""

#Crée une interface
gui = Gui("Recherche GES par Lieux")
gui.init()
