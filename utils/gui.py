"""
Module gui pour créer une interface
"""

# TODO: Enlever ce fichier et utiliser PYSIDE6 a la place
# WARNING: LES IMPORTATIONS RALENTISSENT L'APP IL FAUT TOUJOURS OPTIMISER LES IMPORTATIONS COMME ICI (le preload doit se faire avant un maximum d'importations !)
from tkinter import Tk, Canvas
from tkinter.ttk import Combobox
from tkinter.messagebox import showerror
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.pyplot import subplots, xlabel, ylabel, xticks, close as pltclose
from os.path import isfile
from os import remove
from requests.exceptions import HTTPError
from utils.api import Api
from utils.map import Map
from utils.constants import RESOURCE_PATH
from customtkinter import CTkButton, CTkLabel
from PIL.Image import open as openimg
from PIL.ImageTk import PhotoImage
from PIL.Image import Resampling

class Gui:
    """
    Classe Gui qui génère une interface
    Doc customtkinter: https://customtkinter.tomschimansky.com/documentation/
    """

    # Initialisation de la classe et des fenetres avec ses composants
    def __init__(self, title: str = "Title", resizable: bool = True, tests: bool = False) -> None:
        # Initialisation de l'API
        try:
            self.api = Api()
        except HTTPError as e:
            if tests: raise e
            showerror("Erreur", "Erreur de requete vers l'API: " + str(e.response))

        # Initialisation de la carte
        self.map = Map(self.api)

        # Initialisation des ressources de l'interface
        self.img = openimg(f"{RESOURCE_PATH}\\img\\background.jpg")

        # Initialisation des composants de l'interface
        self.window = Tk()
        self.canvas = Canvas(self.window)
        self.background_photo = None
        self.list_ville = Combobox(self.window, state="readonly")
        self.ville_label = CTkLabel(self.window, text="Type de localité : ", text_color="black", height=20, padx=3, pady=3)
        self.graphic_button = CTkButton(self.window, text="Générer un graphique", command=self.__show_graphic, state="disabled")
        self.map_button = CTkButton(self.window, text="Générer une carte", command=self.__generatemap)
        self.graphic_widget = None

        # Paramètres de l'interface
        self.title = title
        self.resizable = resizable
        self.minsize = (400, 200)
        self.tests = tests

        # Parametres de l'API
        self.data_type = None

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

        self.list_ville.options = ("Régions", "Départements", "Communes")
        self.list_ville.configure(values=self.list_ville.options, justify="center", width=24)
        self.list_ville.bind("<<ComboboxSelected>>", self.__on_selected)
        self.list_ville.current(1)

        self.list_ville.place(relx=0.5, y=30, x=((len(self.ville_label.cget("text"))*2) + 26), anchor="center")
        self.ville_label.place(relx=0.5, y=30, x=-80, anchor="center")
        self.graphic_button.place(relx=0.5, y=80, x=-75, anchor="center")
        self.map_button.place(relx=0.5, y=80, x=80, anchor="center")

        self.canvas.bind('<Configure>', self.__on_resize)
        self.canvas.pack(fill="both", expand=True)

        self.window.iconbitmap(f"{RESOURCE_PATH}\\icons\\icon-x32.ico")

        # Tester si l'interface fonctionne correctement
        if self.tests:
            self.__show_graphic()
            self.__generatemap(False)

            self.close()
        else:
            self.window.mainloop()

    def close(self) -> None:
        """
        Fonction close pour fermer l'interface
        """

        self.window.destroy()

    # Fonction privé qui permet d'afficher le graphique sur l'interface
    def __show_graphic(self) -> None:
        try:
            inputdata = self.list_ville.get()
            data = self.api.getCO2(self.data_type, inputdata)
            dates = list(data.keys())
            totalco2 = list(data.values())

            self.canvas.delete("all") # supprimer l'image de fond

            fig, ax = subplots(num="GES")
            ax.set_title(f"Bilan GES {self.data_type.removesuffix("s")} {inputdata}")
            ax.bar(dates, totalco2, label="CO2")

            xlabel('Dates')
            ylabel('Tonnes de CO2')

            xticks(rotation=90) # dates à la verticale
            ax.legend()

            fig.set_figwidth(fig.get_figwidth() * 1.2)
            fig.set_figheight(fig.get_figheight() * 1.2)

            graphic = FigureCanvasTkAgg(fig, master=self.window)

            if self.graphic_widget is not None:
                self.graphic_widget.destroy()

            self.graphic_widget = graphic.get_tk_widget()
            self.graphic_widget.place(relx=0.5, y=500, anchor="center")

            self.window.minsize(self.minsize[0] + 600, self.minsize[1] + 680)

            pltclose()
        except HTTPError as e:
            if self.tests: raise e
            showerror("Erreur", "Erreur de requete vers l'API: " + str(e.response))

    # Fonction privé pour générer une carte en fonction du CO2
    def __generatemap(self, save: bool = True) -> None:
        if save:
            self.map.save("map.html")

    # Fonction privé (evenement) qui ajuste la position de la barre de selection/change le texte du label en fonction de la valeure sélectionnée
    def __on_selected(self, event) -> None:
        options = self.list_ville["values"]
        selected_index = self.list_ville.current()
        selected_option = options[self.list_ville.current()]

        if options == self.list_ville.options:
            self.data_type = selected_option
            self.graphic_button.configure(state="normal")
            self.ville_label.configure(text=f"{selected_option.removesuffix("s")} : ")
            match selected_option:
                case "Régions":
                    self.list_ville["values"] = ["Retour"] + self.api.regions
                case "Départements":
                    self.list_ville["values"] = ["Retour"] + self.api.departements
                case "Communes":
                    self.list_ville["values"] = ["Retour"] + self.api.communes
            self.list_ville.current(1)
            self.list_ville.place_configure(x=(len(self.ville_label.cget("text"))*2) + 26)
        else:
            if selected_index == 0 and selected_option == "Retour":
                self.ville_label.configure(text="Type de localité : ")
                self.list_ville["values"] = self.list_ville.options
                self.list_ville.current(0)
                self.graphic_button.configure(state="disabled")
            self.list_ville.place_configure(x=(len(self.ville_label.cget("text"))*2) + 26)
    
    # Fonction privé (evenement) qui ajuste la taille du fond lorsque l'on redimentionne la taille de la fenetre
    def __on_resize(self, event) -> None:
        if not self.graphic_widget:
            x = event.width
            y = event.height
            background_image = self.img.resize((x,y), Resampling.BILINEAR)
            self.background_photo = PhotoImage(background_image)
            long, larg = background_image.size

            x = (x - long) // 2
            y = (y - larg) // 2

            self.canvas.delete("all")
            self.canvas.create_image(x, y, image=self.background_photo, anchor="nw")
