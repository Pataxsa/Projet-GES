from utils.libs import checkLibs
checkLibs()
from requests.exceptions import HTTPError
from utils.api import Api
import matplotlib.pyplot as plt

#Fait un graphique de l'évolution du nombre de tonnes de CO2 généré dans une commune spécifique
try:
    inputdata = input("Saisir la commune (écrire \"leave\" pour quitter): ")
    while inputdata.lower().rstrip(" ") != "leave":
        api = Api()
        data = api.getCO2fromcommune(inputdata)
        dates = list(data.keys())
        totalco2 = list(data.values())

        if(len(data) != 0):
            fig, ax = plt.subplots(num="GES")
            ax.set_title(f"Bilan GES commune {inputdata}")
            ax.plot(dates, totalco2, label="CO2")
            plt.xlabel('Dates')
            plt.ylabel('Tonnes de CO2')
            ax.legend()

            plt.show()
        else:
            print(f"Je n'ai trouvé aucune information concernant la commune {inputdata}")
        
        inputdata = input("Saisir la commune (écrire \"leave\" pour quitter): ")
except HTTPError as e:
    print("Erreur de requete vers l'API: " + str(e.response))