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
from utils.map import MAP


class Gui:
    """
    Classe Gui qui génère une interface
    """

    #Initialisation de la classe et des fenetres avec ses composants
    def __init__(self,
                 title: str = "Title",
                 resizable: bool = True,
                 tests: bool = False):
        #Initialisation de l'API
        try:
            self.api = Api()
        except HTTPError as e:
            if tests: raise e
            messagebox.showerror(
                "Erreur", "Erreur de requete vers l'API: " + str(e.response))

        #Initialisation de la carte
        self.map = MAP(self.api)

        #Initialisation des composants de l'interface
        self.window = tk.Tk()
        self.list_ville = ttk.Combobox(self.window,
                                       width=len(self.api.communes[0]) + 5,
                                       state="readonly")
        self.ville_label = tk.Label(self.window, text="Commune :")
        self.research_button = tk.Button(self.window,
                                         text="Rechercher",
                                         command=self.__show_graphic)
        self.map_button = tk.Button(self.window,
                                    text="Générer une carte",
                                    command=self.__generatemap)
        self.graphic_widget = None

        #Paramètres de l'interface
        self.title = title
        self.resizable = resizable
        self.minsize = (400, 200)
        self.tests = tests

        #Parametres de l'API
        self.dataname = "Communes"

    def init(self):
        """
        Fonction init pour lancer une interface
        """

        self.window.title(self.title)
        self.window.resizable(self.resizable, self.resizable)
        self.window.minsize(self.minsize[0], self.minsize[1])

        self.list_ville.config(values=["==COMMUNES=="] + self.api.communes +
                               ["==DEPARTEMENTS=="] + self.api.departements +
                               ["==REGIONS=="] + self.api.regions)
        self.list_ville.bind("<<ComboboxSelected>>", self.__selected)
        self.list_ville.current(1)

        self.list_ville.place(relx=0.5, y=30, anchor="center", x=35)
        self.ville_label.place(relx=0.5, y=30, anchor="center", x=-55)
        self.research_button.place(relx=0.5, y=80, anchor="center", x=-60)
        self.map_button.place(relx=0.5, y=80, anchor="center", x=40)

        self.window.mainloop()

    def testinit(self):
        """
        Fonction testinit pour lancer une interface utilisée pour les tests
        """

        self.window.title(self.title)
        self.window.resizable(self.resizable, self.resizable)
        self.window.minsize(self.minsize[0], self.minsize[1])

        self.list_ville.config(values=["==COMMUNES=="] + self.api.communes +
                               ["==DEPARTEMENTS=="] + self.api.departements)
        self.list_ville.bind("<<ComboboxSelected>>", self.__selected)
        self.list_ville.current(1)

        self.list_ville.place(relx=0.5, y=30, anchor="center", x=35)
        self.ville_label.place(relx=0.5, y=30, anchor="center", x=-55)
        self.research_button.place(relx=0.5, y=80, anchor="center", x=-60)
        self.map_button.place(relx=0.5, y=80, anchor="center", x=40)

        self.__show_graphic()
        self.__generatemap(False)

        self.close()

    #Script a exécuter lorsque l'on clique sur le boutton
    def __show_graphic(self):
        try:
            inputdata = self.list_ville.get()
            data = self.api.tri_France(self.dataname,inputdata)
            dates = list(data.keys())
            totalco2 = list(data.values())

            fig, ax = plt.subplots(num="GES")
            ax.set_title(f"Bilan GES {self.dataname[:-1]} {inputdata}")
            ax.bar(dates, totalco2, label="CO2")

            # Ajout des titres de l'axe x au-dessus des barres
            for i in range(len(dates)):
                ax.text(dates[i],
                        totalco2[i],
                        str(dates[i]),
                        ha='center',
                        va='bottom',
                        rotation=90,
                        fontsize=8)

            plt.xlabel('Dates')
            plt.ylabel('Tonnes de CO2')
            plt.xticks([])
            ax.legend()

            fig.set_figwidth(fig.get_figwidth() * 1.2)
            fig.set_figheight(fig.get_figheight() * 1.2)

            graphic = FigureCanvasTkAgg(fig, master=self.window)

            if self.graphic_widget is not None:
                self.graphic_widget.destroy()

            self.graphic_widget = graphic.get_tk_widget()
            self.graphic_widget.place(relx=0.5, y=500, anchor="center")

            self.window.minsize(self.minsize[0] + 600, self.minsize[1] + 680)

            plt.close()
        except HTTPError as e:
            if self.tests: raise e
            messagebox.showerror(
                "Erreur", "Erreur de requete vers l'API: " + str(e.response))

    #Fonction pour générer une carte en fonction du CO2
    def __generatemap(self, save=True):
        self.map.generate()
        if save:
            self.map.save("map.html")

    #Ajuster la taille de la barre de selection et vérifier si on peux sélectionner la valeur
    def __selected(self, event):
        if self.list_ville.get().startswith("=="):
            self.list_ville.current(1)
            self.dataname = "Communes"
            self.ville_label.config(text="Commune : ")
            self.list_ville.place_configure(x=len(self.list_ville.get()) * 3 +
                                            12)
            self.list_ville.config(width=len(self.list_ville.get()) + 5)
        else:
            self.list_ville.config(width=len(self.list_ville.get()) + 5)

            current = self.list_ville.current()
            values = self.list_ville.config().items().mapping["values"][4]
            if current > values.index(
                    "==COMMUNES==") and current < values.index(
                        "==DEPARTEMENTS=="):
                self.dataname = "Communes"
                self.ville_label.config(text="Commune : ")
                self.list_ville.place_configure(
                    x=len(self.list_ville.get()) * 3 + 12)
            elif current > values.index(
                    "==DEPARTEMENTS==") and current < values.index(
                        "==REGIONS=="):
                self.dataname = "Départements"
                self.ville_label.config(text="Département : ")
                self.list_ville.place_configure(
                    x=len(self.list_ville.get()) * 3 + 14)
            else:
                self.dataname = "Régions"
                self.ville_label.config(text="Région : ")
                self.list_ville.place_configure(
                    x=len(self.list_ville.get()) * 3 + 2)

    def close(self):
        """
        Fonction close pour fermer l'interface
        """

        self.window.destroy()
