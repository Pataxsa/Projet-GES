from requests import get
from requests.exceptions import HTTPError

"""
Classe API pour faire des requetes https
Lien vers la doc API: https://data.ademe.fr/datasets/gnzo7xgwv5d271w1t0yw8ynb/api-doc
"""
class Api:
    #Initialisation (constructeur)
    def __init__(self):
        self.__apilink = "https://data.ademe.fr/data-fair/api/v1/datasets/bilan-ges/"
    
    #Fonction privée pour faire des requetes basiques avec des paramètres
    def __getData(self, link, param):
        if (len(param) >= 1):
            rsp = self.__apilink + link + "?"

            for key, val in param.items():
                if rsp.endswith("?"):
                    rsp += key+"="+str(val)
                else:
                    rsp += "&"+key+"="+str(val)
            
            response = get(rsp)
        else:
            response = get(self.__apilink + link)

        if(not response.ok): raise HTTPError(response=response.content)

        return response.json()
    

    #Fonction publique qui renvoie les informations du fichier CSV de l'API
    def getFile(self):
        return self.__getData("data-files")[0]
    
    #Fonction publique qui renvoie les informations de certaines lignes (en fonction des paramètres)
    def getLines(self, **kwargs):
        return self.__getData("lines", kwargs)