from utils.libs import checkLibs
checkLibs()
from requests.exceptions import HTTPError
from utils.api import Api

#Test de l'api (a continuer)
#Liste toutes les communes disponibles
try:
    results = None
    b = 1
    while results == None or len(results) != 0:
        results = Api().getLines(page=b, qs="type_de_structure:Collectivité territoriale AND type_de_collectivite:Communes", select="raison_sociale")["results"]
        b += 1

        for i in range(len(results)):
            print(results[i])
except HTTPError as e:
    print("Error: " + str(e.response))