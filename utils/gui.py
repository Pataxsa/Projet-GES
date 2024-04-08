"""
Module gui pour créer une interface
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from os.path import isfile
from os import remove
from requests.exceptions import HTTPError
from utils.api import Api
from utils.map import MAP
from customtkinter import CTkButton, CTkLabel
from PIL import Image, ImageTk

class Gui:
    """
    Classe Gui qui génère une interface
    """

    # Initialisation de la classe et des fenetres avec ses composants
    def __init__(self, title: str = "Title", resizable: bool = True, tests: bool = False) -> None:
        # Initialisation de l'API
        try:
            self.api = Api()
        except HTTPError as e:
            if tests: raise e
            messagebox.showerror("Erreur", "Erreur de requete vers l'API: " + str(e.response))

        # Initialisation de la carte
        self.map = MAP(self.api)

        # Initialisation des ressources de l'interface
        self.img = Image.open(f"{self.api.basepath}\\interface\\img\\GES.jpg")

        # Initialisation des composants de l'interface
        self.window = tk.Tk()
        self.canvas = tk.Canvas(self.window)
        self.background_photo = None
        self.list_ville = ttk.Combobox(self.window, width=len(self.api.communes[0]) + 5, state="readonly")
        self.ville_label = CTkLabel(self.window, text="Commune :", text_color="black", height=21)
        self.research_button = CTkButton(self.window, text="Rechercher", command=self.__show_graphic)
        self.map_button = CTkButton(self.window, text="Générer une carte", command=self.__generatemap)
        self.graphic_widget = None

        # Paramètres de l'interface
        self.title = title
        self.resizable = resizable
        self.minsize = (400, 200)
        self.tests = tests

        # Parametres de l'API
        self.dataname = "Communes"

    def init(self) -> None:
        """
        Fonction init pour lancer une interface
        """

        # Supprimer la carte si elle existe (afin de la réactualiser par la suite)
        if isfile("map.html"):
            remove("map.html")

        self.window.title(self.title)
        self.window.resizable(self.resizable, self.resizable)
        self.window.minsize(self.minsize[0], self.minsize[1])

        self.list_ville.configure(values=["==COMMUNES=="] + self.api.communes + ["==DEPARTEMENTS=="] + self.api.departements + ["==REGIONS=="] + self.api.regions)
        self.list_ville.configure(justify='center')
        self.list_ville.bind("<<ComboboxSelected>>", self.__on_selected)
        self.list_ville.current(1)

        self.list_ville.place(relx=0.5, y=30, anchor="center", x=30)
        self.ville_label.place(relx=0.5, y=30, anchor="center", x=-55)
        self.research_button.place(relx=0.5, y=80, anchor="center", x=-90)
        self.map_button.place(relx=0.5, y=80, anchor="center", x=55)

        self.canvas.bind('<Configure>', self.__on_resize)
        self.canvas.pack(fill="both", expand=True)

        self.window.mainloop()

    def testinit(self) -> None:
        """
        Fonction testinit pour lancer une interface utilisée pour les tests
        """

        self.window.title(self.title)
        self.window.resizable(self.resizable, self.resizable)
        self.window.minsize(self.minsize[0], self.minsize[1])

        self.list_ville.configure(values=["==COMMUNES=="] + self.api.communes + ["==DEPARTEMENTS=="] + self.api.departements + ["==REGIONS=="] + self.api.regions)
        self.list_ville.bind("<<ComboboxSelected>>", self.__on_selected)
        self.list_ville.current(1)

        self.list_ville.place(relx=0.5, y=30, anchor="center", x=35)
        self.ville_label.place(relx=0.5, y=30, anchor="center", x=-55)
        self.research_button.place(relx=0.5, y=80, anchor="center", x=-60)
        self.map_button.place(relx=0.5, y=80, anchor="center", x=40)

        self.__show_graphic()
        self.__generatemap(False)

        self.close()

    def close(self) -> None:
        """
        Fonction close pour fermer l'interface
        """

        self.window.destroy()

    # Fonction privé qui permet d'afficher le graphique sur l'interface
    def __show_graphic(self) -> None:
        try:
            inputdata = self.list_ville.get()
            data = self.api.getCO2(self.dataname, inputdata)
            dates = list(data.keys())
            totalco2 = list(data.values())

            self.canvas.delete("all") # supprimer l'image de fond

            fig, ax = plt.subplots(num="GES")
            ax.set_title(f"Bilan GES {self.dataname[:-1]} {inputdata}")
            ax.bar(dates, totalco2, label="CO2")

            plt.xlabel('Dates')
            plt.ylabel('Tonnes de CO2')

            plt.xticks(rotation=90) # dates à la verticale
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
            messagebox.showerror("Erreur", "Erreur de requete vers l'API: " + str(e.response))

    # Fonction privé pour générer une carte en fonction du CO2
    def __generatemap(self, save: bool = True) -> None:
        if save:
            self.map.save("map.html")

    # Fonction privé (evenement) qui ajuste la taille de la barre de selection
    def __on_selected(self, event) -> None:
        if self.list_ville.get().startswith("=="):
            self.list_ville.current(1)
            self.dataname = "Communes"
            self.ville_label.configure(text="Commune : ")
            self.list_ville.place_configure(x=(len(self.list_ville.get()) * 3) + 12)
            self.list_ville.configure(width=len(self.list_ville.get()) + 5)
        else:
            self.list_ville.configure(width=len(self.list_ville.get()) + 5)

            current = self.list_ville.current()
            values = self.list_ville.configure().items().mapping["values"][4]
            if current > values.index("==COMMUNES==") and current < values.index("==DEPARTEMENTS=="):
                self.dataname = "Communes"
                self.ville_label.configure(text="Commune : ")
                self.list_ville.place_configure(x=len(self.list_ville.get()) * 3 + 12)
            elif current > values.index("==DEPARTEMENTS==") and current < values.index("==REGIONS=="):
                self.dataname = "Départements"
                self.ville_label.configure(text="Département : ")
                self.list_ville.place_configure(x=(len(self.list_ville.get()) * 3) + 14)
            else:
                self.dataname = "Régions"
                self.ville_label.configure(text="Région : ")
                self.list_ville.place_configure(x=(len(self.list_ville.get()) * 3) + 2)
    
    # Fonction privé (evenement) qui ajuste la taille du fond lorsque l'on redimentionne la taille de la fenetre
    def __on_resize(self, event) -> None:
        if not self.graphic_widget:
            x = event.width
            y = event.height
            background_image = self.img.resize((x,y),Image.Resampling.BILINEAR)
            self.background_photo = ImageTk.PhotoImage(background_image)
            long, larg = background_image.size

            x = (x - long) // 2
            y = (y - larg) // 2

            self.canvas.delete("all")
            self.canvas.create_image(x,y , image=self.background_photo, anchor="nw")