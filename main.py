from utils.libs import checkLibs
checkLibs()
from requests.exceptions import HTTPError
from utils.api import Api
import matplotlib.pyplot as plt

#Fait un graphique de l'évolution du nombre de tonnes de CO2 généré dans une commune spécifique
try:
    api = Api()
    params = [b for b in api.params if "emissions_publication_p" in b]
    commune = "Paris" #nom de la commune
    lines = api.getLines(select=["date_de_publication"]+params, size=api.maxlines, qs=f"type_de_structure: Collectivité territoriale AND type_de_collectivite:Communes AND raison_sociale:\"{commune}\" AND date_de_publication:[2003-01-01 TO 2024-12-31]")

    dates = [date["date_de_publication"] for date in lines]

    result = 0
    data = []
    for val in lines:
        dt = 0
        for param in params:
            if param in val.keys():
                dt += val[param]
        data.append(dt)
    
    fig, ax = plt.subplots(num="GES")
    ax.set_title(f"Bilan GES commune {commune}")
    ax.plot(dates, data, label="CO2")
    plt.xlabel('Dates')
    plt.ylabel('Tonnes de CO2')
    ax.legend()

    plt.show()
except HTTPError as e:
    print("Error: " + str(e.response))