"""
Module gui pour créer une interface
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from requests.exceptions import HTTPError
from utils.api import Api


class Gui:
    """
    Classe Gui qui génère une interface
    """

    #Initialisation de la classe et des fenetres avec ses composants
    def __init__(self, title:str = "Title", resizable:bool = True):
        #Initialisation de l'API
        try:
            self.api = Api()
        except HTTPError as e:
            messagebox.showerror("Erreur", "Erreur de requete vers l'API: " + str(e.response))

        #Initialisation des composants de l'interface
        self.window = tk.Tk()
        self.list_ville = ttk.Combobox(self.window, width=len(self.api.communes[0])+5, state="readonly")
        self.ville_label = tk.Label(self.window, text="Commune :")
        self.research_button = tk.Button(self.window, text="Rechercher", command=self.__show_graphic)
        self.graphic_widget = None

        #Paramètres de l'interface
        self.title = title
        self.resizable = resizable
        self.minsize = (400, 200)

        #Parametres de l'API
        self.dataname = "Communes"


    def init(self):
        """
        Fonction init pour lancer une interface
        """

        self.window.title(self.title)
        self.window.resizable(self.resizable, self.resizable)
        self.window.minsize(self.minsize[0], self.minsize[1])

        self.list_ville.config(values=["==COMMUNES=="] + self.api.communes + ["==DEPARTEMENTS=="] + self.api.departements)
        self.list_ville.bind("<<ComboboxSelected>>", self.__selected)
        self.list_ville.current(1)

        self.list_ville.place(relx=0.5, y=30, anchor="center", x=35)
        self.ville_label.place(relx=0.5, y=30, anchor="center", x=-55)
        self.research_button.place(relx=0.5, y=80, anchor="center")

        self.window.mainloop()


    def testinit(self):
        """
        Fonction testinit pour lancer une interface utilisée pour les tests
        """

        self.window.title(self.title)
        self.window.resizable(self.resizable, self.resizable)
        self.window.minsize(self.minsize[0], self.minsize[1])

        self.list_ville.config(values=["==COMMUNES=="] + self.api.communes + ["==DEPARTEMENTS=="] + self.api.departements)
        self.list_ville.bind("<<ComboboxSelected>>", self.__selected)
        self.list_ville.current(1)

        self.list_ville.place(relx=0.5, y=30, anchor="center", x=35)
        self.ville_label.place(relx=0.5, y=30, anchor="center", x=-55)
        self.research_button.place(relx=0.5, y=80, anchor="center")

        self.__show_graphic()

        self.close()


    #Script a exécuter lorsque l'on clique sur le boutton
    def __show_graphic(self):
        try:
            inputdata = self.list_ville.get()
            data = self.api.getCO2(self.dataname, inputdata)
            dates = list(data.keys())
            totalco2 = list(data.values())

            fig, ax = plt.subplots(num="GES")
            ax.set_title(f"Bilan GES {self.dataname[:-1]} {inputdata}")
            ax.bar(dates, totalco2, label="CO2")
            plt.xlabel('Dates')
            plt.ylabel('Tonnes de CO2')
            plt.xticks(dates, data, rotation=90)
            plt.tick_params(axis='x', which='major', labelsize=6)
            ax.legend()

            fig.set_figwidth(fig.get_figwidth()*1.5)
            fig.set_figheight(fig.get_figheight()*1.5)

            graphic = FigureCanvasTkAgg(fig, master=self.window)

            if self.graphic_widget is not None:
                self.graphic_widget.grid_remove()

            self.graphic_widget = graphic.get_tk_widget()
            self.graphic_widget.place(relx=0.5, y=500, anchor="center")

            self.window.minsize(self.minsize[0]+600, self.minsize[1]+680)

            plt.close()
        except HTTPError as e:
            messagebox.showerror("Erreur", "Erreur de requete vers l'API: " + str(e.response))


    #Ajuster la taille de la barre de selection et vérifier si on peux sélectionner la valeur
    def __selected(self, event):
        if self.list_ville.get().startswith("=="):
            self.list_ville.current(1)
            self.dataname = "Communes"
        else:
            self.list_ville.config(width=len(self.list_ville.get())+5)
            self.list_ville.place_configure(x=len(self.list_ville.get())*3+12)

            #TODO: souci au niveau de la sélection (plusieurs valeures sont les mêmes ex: dans self.api.communes il y a Paris et aussi dans self.api.departements)
            if self.list_ville.get() in self.api.communes:
                self.dataname = "Communes"
            else:
                self.dataname = "Départements"


    def close(self):
        """
        Fonction close pour fermer l'interface
        """

        self.window.destroy()
