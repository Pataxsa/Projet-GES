import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from requests.exceptions import HTTPError
from utils.api import Api

"""
Classe GUI pour générer une interface
"""
class Gui:
    #Initialisation de la classe et des fenetres avec ses composants
    def __init__(self, title:str = "Title", resizable:bool = True):
        #Initialisation de l'API
        self.api = Api()

        #Initialisation des composants de l'interface
        self.window = tk.Tk()
        self.list_ville = ttk.Combobox(self.window, width=len(self.api.communes[0])+5, state="readonly")
        self.ville_label = tk.Label(self.window, text="Commune :")
        self.research_button = tk.Button(self.window, text="Rechercher", command=self.__show_graphic)
        self.graphic_widget = None

        #Paramètres de l'interface
        self.title = title
        self.resizable = resizable


    #Lancement de la fenetre
    def init(self):
        self.window.title(self.title)
        self.window.resizable(self.resizable, self.resizable)

        self.list_ville.config(values=self.api.communes)
        self.list_ville.bind("<<ComboboxSelected>>", self.__selected)
        self.list_ville.current(0)

        self.list_ville.grid(row=0, column=1)
        self.ville_label.grid(row=0, column=0)
        self.research_button.grid(row=1, column=0, columnspan=2, pady=10)

        self.window.mainloop()
    

    #Tests de l'initialisation
    def testinit(self):
        self.window.title(self.title)
        self.window.resizable(self.resizable, self.resizable)

        self.list_ville.config(values=self.api.communes)
        self.list_ville.bind("<<ComboboxSelected>>", self.__selected)
        self.list_ville.current(0)

        self.list_ville.grid(row=0, column=1)
        self.ville_label.grid(row=0, column=0)
        self.research_button.grid(row=1, column=0, columnspan=2, pady=10)

        self.close()
        

    #Script a exécuter lorsque l'on clique sur le boutton
    def __show_graphic(self):
        try:
            inputdata = self.list_ville.get()
            data = self.api.getCO2("Communes", inputdata)
            dates = list(data.keys())
            totalco2 = list(data.values())

            fig, ax = plt.subplots(num="GES")
            ax.set_title(f"Bilan GES commune {inputdata}")
            ax.bar(dates, totalco2, label="CO2")
            plt.xlabel('Dates')
            plt.ylabel('Tonnes de CO2')
            ax.legend()

            graphic = FigureCanvasTkAgg(fig, master=self.window)

            if self.graphic_widget != None:
                self.graphic_widget.grid_remove()

            self.graphic_widget = graphic.get_tk_widget()
            self.graphic_widget.grid(row=3, column=0, columnspan=2, pady=10)

            plt.close()
        except HTTPError as e:
            messagebox.showerror("Erreur", "Erreur de requete vers l'API: " + str(e.response))
    
    #Ajuster la taille de la barre de selection (car sinon on ne vois pas bien)
    def __selected(self, event):
        self.list_ville.config(width=len(self.list_ville.get())+5)
    
    #Fonction pour fermer la fenetre
    def close(self):
        self.window.destroy()