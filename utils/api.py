"""
Module api pour générer la base de l'API

Module : 
    requests_cache.CachedSession : Pour stocker les données en locales et les actualisé (éviter de refaire des requêtes)
    requests.exceptions.HTTPError : Pour lever des erreurs en cas de problème lors des requêtes
    requests.exceptions.ConnectionError : Condition pour HTTPError

    typing.Any :

    API_LINK :
    ROOT_PATH :
    REQUEST_CACHE_EXPIRE :
"""

from requests_cache import CachedSession
from requests.exceptions import HTTPError, ConnectionError
from typing import Any

from utils.constants import API_LINK, ROOT_PATH, REQUEST_CACHE_EXPIRE

class Api:
    """
    Classe API pour faire des requetes https
    Lien vers la doc API: https://data.ademe.fr/datasets/gnzo7xgwv5d271w1t0yw8ynb/api-doc
    """

    # Initialisation (constructeur)
    def __init__(self) -> None:
        # Parametres de l'API
        self.maxlines: int = 10000
        self.minlines: int = 1
        self.params: list[str] = [
            'id', 'methode_beges_v4v5', 'date_de_publication',
            'type_de_structure', 'type_de_collectivite', 'raison_sociale',
            'siren_principal', 'apenaf_associe', 'libelle',
            'nombre_de_salariesdagents', 'population', 'region',
            'code_departement', 'departement', 'structure_obligee',
            'mode_de_consolidation', 'annee_de_reporting',
            'assujetti_dpefpcaet', 'aide_diag_decarbonaction',
            'seuil_dimportance_retenu_percent', 'niveau_dinfluence',
            'importance_strategique_et_vulnerabilites',
            'lignes_directrices_specifiques_au_secteur', 'soustraitance',
            'engagement_du_personnel', 'emissions_publication_p11',
            'emissions_publication_p12', 'emissions_publication_p13',
            'emissions_publication_p14', 'emissions_publication_p15',
            'emissions_publication_p21', 'emissions_publication_p22',
            'emissions_publication_p31', 'emissions_publication_p32',
            'emissions_publication_p33', 'emissions_publication_p34',
            'emissions_publication_p35', 'emissions_publication_p41',
            'emissions_publication_p42', 'emissions_publication_p43',
            'emissions_publication_p44', 'emissions_publication_p45',
            'emissions_publication_p51', 'emissions_publication_p52',
            'emissions_publication_p53', 'emissions_publication_p54',
            'emissions_publication_p61',
            'une_annee_de_reference_a_ete_calculee', 'emissions_reference_p11',
            'emissions_reference_p12', 'emissions_reference_p13',
            'emissions_reference_p14', 'emissions_reference_p15',
            'emissions_reference_p21', 'emissions_reference_p22',
            'emissions_reference_p31', 'emissions_reference_p32',
            'emissions_reference_p33', 'emissions_reference_p34',
            'emissions_reference_p35', 'emissions_reference_p41',
            'emissions_reference_p42', 'emissions_reference_p43',
            'emissions_reference_p44', 'emissions_reference_p45',
            'emissions_reference_p51', 'emissions_reference_p52',
            'emissions_reference_p53', 'emissions_reference_p54',
            'emissions_reference_p61', 'objectif_emissions_directes',
            'objectif_emissions_indirectes_significatives',
            'part_de_lenergie_garantie_dorigine_etou_renouvelable_dans_la_consommation_denergie',
            'responsable_du_suivi', 'fonction', 'telephone', 'courriel', '_id',
            '_i', '_rand'
        ]

        # Session utilisant le cache pour les requetes
        self.__session = CachedSession(cache_name=f"{ROOT_PATH}\\cache\\request-cache", expire_after=REQUEST_CACHE_EXPIRE)
        
        # Nom des communes/departements/regions + données totale (self.france)
        self.france: list[dict[str, int | str]] = self.__getLines(select=["raison_sociale", "departement", "region", "type_de_structure", "type_de_collectivite", "date_de_publication"] + [b for b in self.params if "emissions_publication_p" in b], size=self.maxlines)
        communes: list[str] = sorted({com["raison_sociale"] for com in self.france if com.get("type_de_collectivite") == "Communes" and com.get("type_de_structure") == "Collectivité territoriale (dont EPCI)"})
        departements: list[str] = sorted({dep["departement"] for dep in self.france})
        regions: list[str] = sorted({reg["region"] for reg in self.france})
        self.locality_names: dict[str, list[str]] = {"Communes": communes, "Departements": departements, "Regions": regions}

        self.__session.close()
        
    # Fonction privée pour faire des requetes basiques avec des paramètres
    def __getData(self, link: str, param: dict[str, Any]) -> dict[str, int | list]:
        try:
            url = API_LINK + link
            response = self.__session.get(url, params=param) if param else self.__session.get(url)
        except ConnectionError:
            raise HTTPError(response="Connexion impossible")

        if (not response.ok): raise HTTPError(response=response._content)

        return response.json()

    # Fonction privé qui renvoie les informations de certaines lignes (en fonction des paramètres, utiliser le parametre size pour prendre en compte plus de valeurs)
    def __getLines(self, select: list[str] = None, **kwargs) -> list[dict[str, int | str]]:
        if select:
            kwargs["select"] = ",".join(select)

        return self.__getData("lines", kwargs)["results"]
    
    def getCO2(self, type_data: str, nom: str) -> dict[str, int]:
        """
        Fonction getCO2 qui renvoie le CO2 total par année d'un lieu (renvoie un dictionnaire clés:années et valeurs:total co2)
        """

        params = [b for b in self.params if "emissions_publication_p" in b]
        type_data_key = type_data.lower().replace("é", "e").removesuffix("s")
        dates_co2 = {}

        for val in self.france:
            if (type_data in ["Régions", "Départements"] and val[type_data_key] == nom) or (type_data == "Communes" and val.get("type_de_structure") == "Collectivité territoriale (dont EPCI)" and val.get("type_de_collectivite") == "Communes" and val["raison_sociale"] == nom):
                date = val["date_de_publication"].split("-")[0]
                totalco2 = sum(val[param] for param in params if param in val)
                            
                dates_co2[date] = dates_co2.get(date, 0) + totalco2

        return dates_co2

    def getCO2Total(self, type_data: str) -> dict[str, int]:
        """
        Fonction getCO2Total qui renvoie le CO2 total (toutes les dates) d'un lieu (renvoie un dictionnaire clés:nom et valeurs:total co2)
        """

        params = [b for b in self.params if "emissions_publication_p" in b]
        type_data_key = type_data.lower().replace("é", "e").removesuffix("s")
        data = {}

        for val in self.france:
            nom = val[type_data_key]
            totalco2 = sum(val[param] for param in params if param in val)

            data[nom] = data.get(nom, 0) + totalco2

        return data
