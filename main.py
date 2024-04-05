"""
Module main pour créer et lancer l'interface
"""

import subprocess
from utils.gui import Gui

#Installation des modules nécessaires

modules = ['folium','branca','requests','matplotlib','customtkinter']
possession = subprocess.run(["pip", "list"], capture_output=True, text=True).stdout.split()
possession = [possession[i] for i in range(0,len(possession),2)]




for i in modules:
    if not i in possession:
        try:
            subprocess.run(["pip","install","poetry"])
            subprocess.run(["poetry","install"])

            print("Poetry a été installé avec succès!")
            break

        except subprocess.CalledProcessError as e:
            print(f"Une erreur s'est produite lors de l'installation de Poetry : {e}")


#Crée une interface
gui = Gui("Recherche GES par Lieux")
gui.init()
