from utils.libs import checkLibs
checkLibs()
from requests.exceptions import HTTPError
from utils.api import Api

#Test de l'api (a continuer)
try:
    print(Api().getLines(size=1))
except HTTPError as e:
    print("Error: " + str(e.response))