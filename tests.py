"""
Module tests pour tester l'interface
"""

import tkinter as tk
from tkinter import ttk
from utils.gui import Gui

def test():
    """
    Effectue un test de l'initialisation
    """

    gui = Gui("Recherche GES par Ville", tests=True)
    gui.testinit()
    

# Dictionnaire contenant les options supplémentaires pour chaque type de localité
options_supplementaires = {
    "Départements": ["Ain", "Aisne", "Allier", "Alpes-de-Haute-Provence", "Alpes-Maritimes", "Ardèche", "Ardennes"],
    "Régions": ["Auvergne-Rhône-Alpes", "Bourgogne-Franche-Comté", "Bretagne", "Centre-Val de Loire", "Corse"],
    "Communes": ["Paris", "Marseille", "Lyon", "Toulouse", "Nice", "Nantes", "Strasbourg"]
}

# Liste des types principaux
types_principaux = ["options","Départements", "Régions", "Communes"]

def on_combo_changed(event):
    selected_index = combo.current()
    if selected_index == 0 :
        combo['values'] = types_principaux
    elif selected_index < len(types_principaux):

        selected_type = types_principaux[selected_index]
        child_options = options_supplementaires.get(selected_type, [])
        combo['values'] = ["choix des options"] + child_options

root = tk.Tk()
root.title("Combobox dynamique")


frame = ttk.Frame(root)
frame.pack(padx=50, pady=25)

# Label pour le type de localité
label_type = ttk.Label(frame, text="Type de localité :")
label_type.grid(row=0, column=0, padx=(0, 10), sticky=tk.E)

# Combobox pour sélectionner le type de localité
combo = ttk.Combobox(frame, values=types_principaux)
combo.grid(row=0, column=1, padx=(0, 10), pady=10)

combo.bind("<<ComboboxSelected>>", on_combo_changed)

root.mainloop()





