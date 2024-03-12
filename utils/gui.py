import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from requests.exceptions import HTTPError
from utils.api import Api

class Gui:
    #Initialisation de la classe et des fenetres avec ses composants
    def __init__(self, title = "Title", resizable = True):
        #Initialisation des composants de l'interface
        self.window = tk.Tk()
        self.input_ville = tk.Entry(self.window)
        self.ville_label = tk.Label(self.window, text="Commune (leave pour quitter):")
        self.error_label = tk.Label(self.window, text="", fg="red")
        self.research_button = tk.Button(self.window, text="Rechercher", command=self.__recherche_affichage_ges)
        self.graphic_widget = None

        #Paramètres de l'interface
        self.title = title
        self.resizable = resizable

        #Initialisation de l'API
        self.api = Api()


    #Lancement de la fenetre
    def init(self):
        self.window.title(self.title)
        self.window.resizable(self.resizable, self.resizable)

        self.ville_label.grid(row=0, column=0)
        self.error_label.grid(row=2, column=0, columnspan=2, pady=10)
        self.input_ville.grid(row=0, column=1, padx=10, pady=10)
        self.research_button.grid(row=1, column=0, columnspan=2, pady=10)

        self.window.mainloop()
        

    #Script a exécuter lorsque l'on clique sur le boutton
    def __recherche_affichage_ges(self):
        try:
            inputdata = self.input_ville.get()
            if inputdata != "": 
                data = self.api.getCO2fromcommune(inputdata)
                dates = list(data.keys())
                totalco2 = list(data.values())

                if (len(data) != 0):
                    self.error_label.config(text="")

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
                else:
                    if self.graphic_widget != None:
                        self.graphic_widget.grid_remove()
                        self.graphic_widget = None

                    self.error_label.config(
                        text=
                        f"Aucune information trouvée pour la commune {inputdata}")
            else:
                if self.graphic_widget != None:
                        self.graphic_widget.grid_remove()
                        self.graphic_widget = None
                        
                self.error_label.config(
                        text=
                        f"Veuillez mettre un nom de commune")
        except HTTPError as e:
            print("Erreur de requete vers l'API: " + str(e.response))