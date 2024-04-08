"""
Module api pour générer la base de l'API
"""

from requests import get
from requests.exceptions import HTTPError, ConnectionError
import sys

class Api:
    """
    Classe API pour faire des requetes https
    Lien vers la doc API: https://data.ademe.fr/datasets/gnzo7xgwv5d271w1t0yw8ynb/api-doc
    """

    # Initialisation (constructeur)
    def __init__(self) -> None:
        # Parametres de l'API
        self.__apilink = "https://data.ademe.fr/data-fair/api/v1/datasets/bilan-ges/"
        self.maxlines = 10000
        self.minlines = 1
        self.params = [
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

        # Base du chemin d'accès pour les ressources
        self.basepath = getattr(sys, '_MEIPASS', ".")
        
        # Nom des communes/departements/regions + données totale (self.france)
        self.france = self.__getLines(select=["raison_sociale", "departement", "region", "type_de_structure","type_de_collectivite","date_de_publication"] + [b for b in self.params if "emissions_publication_p" in b],size=self.maxlines)
        self.communes = sorted(set([com["raison_sociale"] for com in self.france if "type_de_collectivite" in com.keys() and "type_de_structure" in com.keys() and com["type_de_collectivite"] == "Communes" and com["type_de_structure"] == "Collectivité territoriale (dont EPCI)"]))
        self.departements = sorted(set([dep["departement"] for dep in self.france]))
        self.regions = sorted(set([reg["region"] for reg in self.france]))
        
    # Fonction privée pour faire des requetes basiques avec des paramètres
    def __getData(self, link: str, param: dict) -> dict:
        try:
            if (len(param) >= 1):
                rsp = self.__apilink + link + "?"

                for (index, (key, val)) in enumerate(param.items()):
                    rsp += f"&{key}={val}" if index >= 1 else f"{key}={val}"

                response = get(rsp)
            else:
                response = get(self.__apilink + link)
        except ConnectionError as e:
            raise HTTPError(response="Connexion impossible")

        if (not response.ok): raise HTTPError(response=response._content)

        return response.json()

    # Fonction privé qui renvoie les informations de certaines lignes (en fonction des paramètres, utiliser le parametre size pour prendre en compte plus de valeurs)
    def __getLines(self, select: list = None, **kwargs) -> list:
        if (select != None):
            data = ""
            for val in select:
                data += "%2C" + val
            data = data.removeprefix("%2C")
            kwargs.update({"select": data})

        return self.__getData("lines", kwargs)["results"]
    
    def getCO2(self, type_data: str, nom: str) -> dict:
        """
        Fonction getCO2 qui renvoie le CO2 total par année d'un lieu (renvoie un dictionnaire clés:années et valeurs:total co2)
        """

        params = [b for b in self.params if "emissions_publication_p" in b]
        dates_co2 = {}

        match type_data:
            case "Départements":
                    for val in self.france:
                        date = val["date_de_publication"].split("-")[0]
                        totalco2 = 0
                        if val["departement"] == nom:
                            for param in params:
                                if param in val.keys():
                                    totalco2 += val[param]
                            if date in dates_co2.keys():
                                dates_co2.update({date: dates_co2[date]+totalco2})
                            else:
                                dates_co2.update({date: totalco2})
            case "Régions":
                for val in self.france:
                        date = val["date_de_publication"].split("-")[0]
                        totalco2 = 0
                        if val["region"] == nom:
                            for param in params:
                                if param in val.keys():
                                    totalco2 += val[param]
                            if date in dates_co2.keys():
                                dates_co2.update({date: dates_co2[date]+totalco2})
                            else:
                                dates_co2.update({date: totalco2})
            case "Communes":
                for val in self.france:
                        date = val["date_de_publication"].split("-")[0]
                        totalco2 = 0
                        #vérification des clés car certaines clés n'existent pas
                        if "type_de_collectivite" in val.keys() and "type_de_structure" in val.keys() and val["type_de_structure"] == "Collectivité territoriale (dont EPCI)" and val["type_de_collectivite"] == "Communes" and val["raison_sociale"] == nom:
                            for param in params:
                                if param in val.keys():
                                    totalco2 += val[param]
                            if date in dates_co2.keys():
                                dates_co2.update({date: dates_co2[date]+totalco2})
                            else:
                                dates_co2.update({date: totalco2})

        return dates_co2

    def getCO2Total(self, type_structure: str) -> dict:
        """
        Fonction getCO2Total qui renvoie le CO2 total (toutes les dates) d'un lieu (renvoie un dictionnaire clés:nom et valeurs:total co2)
        """

        params = [b for b in self.params if "emissions_publication_p" in b]
        dataname = None

        match type_structure:
            case "Départements":
                dataname = "departement"
            case "Régions":
                dataname = "region"

        data = {}

        for val in self.france:
            nom = val[dataname]
            totalco2 = 0

            for param in params:
                if param in val.keys():
                    totalco2 += val[param]

            if nom not in data.keys():
                data.update({nom: totalco2})
            else:
                data.update({nom: data.get(nom) + totalco2})

        return data
