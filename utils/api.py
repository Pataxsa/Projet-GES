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
        self.maxlines = 10000
        self.minlines = 1
        self.params = ['id', 'methode_beges_v4v5', 'date_de_publication', 'type_de_structure', 'type_de_collectivite', 'raison_sociale', 'siren_principal', 'apenaf_associe', 'libelle', 'nombre_de_salariesdagents', 'population', 'region', 'code_departement', 'departement', 'structure_obligee', 'mode_de_consolidation', 'annee_de_reporting', 'assujetti_dpefpcaet', 'aide_diag_decarbonaction', 'seuil_dimportance_retenu_percent', 'niveau_dinfluence', 'importance_strategique_et_vulnerabilites', 'lignes_directrices_specifiques_au_secteur', 'soustraitance', 'engagement_du_personnel', 'emissions_publication_p11', 'emissions_publication_p12', 'emissions_publication_p13', 'emissions_publication_p14', 'emissions_publication_p15', 'emissions_publication_p21', 'emissions_publication_p22', 'emissions_publication_p31', 'emissions_publication_p32', 'emissions_publication_p33', 'emissions_publication_p34', 'emissions_publication_p35', 'emissions_publication_p41', 'emissions_publication_p42', 'emissions_publication_p43', 'emissions_publication_p44', 'emissions_publication_p45', 'emissions_publication_p51', 'emissions_publication_p52', 'emissions_publication_p53', 'emissions_publication_p54', 'emissions_publication_p61', 'une_annee_de_reference_a_ete_calculee', 'emissions_reference_p11', 'emissions_reference_p12', 'emissions_reference_p13', 'emissions_reference_p14', 'emissions_reference_p15', 'emissions_reference_p21', 'emissions_reference_p22', 'emissions_reference_p31', 'emissions_reference_p32', 'emissions_reference_p33', 'emissions_reference_p34', 'emissions_reference_p35', 'emissions_reference_p41', 'emissions_reference_p42', 'emissions_reference_p43', 'emissions_reference_p44', 'emissions_reference_p45', 'emissions_reference_p51', 'emissions_reference_p52', 'emissions_reference_p53', 'emissions_reference_p54', 'emissions_reference_p61', 'objectif_emissions_directes', 'objectif_emissions_indirectes_significatives', 'part_de_lenergie_garantie_dorigine_etou_renouvelable_dans_la_consommation_denergie', 'responsable_du_suivi', 'fonction', 'telephone', 'courriel', '_id', '_i', '_rand']
        self.communes = sorted(list(set([commune["raison_sociale"] for commune in self.getLines(select=["raison_sociale"], qs="type_de_structure: Collectivité territoriale AND type_de_collectivite:Communes", size=self.maxlines)])))

        # TODO: Pour plus tard
        self.departements = sorted(list(set([departement["raison_sociale"] for departement in self.getLines(select=["raison_sociale"], qs="type_de_structure: Collectivité territoriale AND type_de_collectivite:Départements", size=self.maxlines)])))
    
    #Fonction privée pour faire des requetes basiques avec des paramètres
    def __getData(self, link:str, param:dict):
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

        if(not response.ok): raise HTTPError(response=response._content)

        return response.json()
    
    #Fonction publique qui renvoie les informations de certaines lignes (en fonction des paramètres, utiliser le parametre size pour prendre en compte plus de valeurs)
    def getLines(self, select:list = None, **kwargs):
        if(select != None):
            data = ""
            for val in select:
                data += "%2C"+val
            data = data.removeprefix("%2C")
            kwargs.update({"select": data})
        
        return self.__getData("lines", kwargs)["results"]
    
    #Fonction publique qui renvoie le CO2 total par année d'une commune (renvoie un dictionnaire clés:années et valeurs:total co2)
    def getCO2fromcommune(self, commune:str = ""):
        params = [b for b in self.params if "emissions_publication_p" in b]
        lines = self.getLines(select=["date_de_publication"]+params, size=self.maxlines, qs=f"type_de_structure: Collectivité territoriale AND type_de_collectivite:Communes AND raison_sociale:\"{commune}\"")

        data = {}

        for val in lines:
            date = val["date_de_publication"]
            totalco2 = 0

            for param in params:
                if param in val.keys():
                    totalco2 += val[param]
                    
            data.update({date: totalco2})
        
        return data