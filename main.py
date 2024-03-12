from utils.libs import checkLibs
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

checkLibs()
from requests.exceptions import HTTPError
from utils.api import Api
import matplotlib.pyplot as plt


#Fait un graphique de l'évolution du nombre de tonnes de CO2 généré dans une commune spécifique
def recherche_affichage_ges():
    try:
        inputdata = entry_ville.get().capitalize()
        while inputdata.lower().rstrip(" ") != "leave":
            api = Api()
            data = api.getCO2fromcommune(inputdata)
            dates = list(data.keys())
            totalco2 = list(data.values())

            if (len(data) != 0):
                fig, ax = plt.subplots(num="GES")
                ax.set_title(f"Bilan GES commune {inputdata}")
                ax.plot(dates, totalco2, label="CO2")
                plt.xlabel('Dates')
                plt.ylabel('Tonnes de CO2')
                ax.legend()

                canvas = FigureCanvasTkAgg(fig, master=fenetre)
                canvas_widget = canvas.get_tk_widget()
                canvas_widget.grid(row=3, column=0, columnspan=2, pady=10)

            else:
                erreur_label.config(
                    text=
                    f"Aucune information trouvée pour la commune {inputdata}")

            inputdata = input(
                "Saisir la commune (écrire \"leave\" pour quitter): ")
        fenetre.destroy()
    except HTTPError as e:
        print("Erreur de requete vers l'API: " + str(e.response))


def interface():
    global entry_ville
    global erreur_label
    global fenetre
    fenetre = tk.Tk()
    fenetre.title("Recherche GES par Ville")

    etiquette_ville = tk.Label(fenetre, text="Commune (leave pour quitter):")
    entry_ville = tk.Entry(fenetre)
    erreur_label = tk.Label(fenetre, text="", fg="red")

    bouton_rechercher = tk.Button(fenetre,
                                  text="Rechercher",
                                  command=recherche_affichage_ges)
    etiquette_ville.grid(row=0, column=0, padx=10, pady=10)
    erreur_label.grid(row=2, column=0, columnspan=2, pady=10)
    entry_ville.grid(row=0, column=1, padx=10, pady=10)
    bouton_rechercher.grid(row=1, column=0, columnspan=2, pady=10)

    fenetre.mainloop()


interface()
