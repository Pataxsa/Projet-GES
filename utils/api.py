from requests import get
from requests.exceptions import HTTPError, ConnectionError
import sys
from concurrent.futures import ThreadPoolExecutor,as_completed

class Api:
    """
    Classe API pour faire des requetes https
    Lien vers la doc API: https://data.ademe.fr/datasets/gnzo7xgwv5d271w1t0yw8ynb/api-doc
    """

    def __init__(self):
        self.__apilink = "https://data.ademe.fr/data-fair/api/v1/datasets/bilan-ges/"
        self.maxlines = 10000
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

        # Récupération des données de manière asynchrone
        self.france = self.fetch_data()
        self.communes = self.filter_communes()
        self.departements = self.filter_departements()
        self.regions = self.filter_regions()

    def __getData(self, link, param):
        try:
            if param:
                rsp = self.__apilink + link + "?" + "&".join(f"{key}={val}" for key, val in param.items())
            else:
                rsp = self.__apilink + link

            response = get(rsp)
            response.raise_for_status()

            return response.json()
        except (ConnectionError, HTTPError) as e:
            raise HTTPError(response=f"Connexion impossible: {e}")

    def make_requests(self, urls):
        """
        Fait des requêtes en parallèle et renvoie les résultats
        """
        results = []
        with ThreadPoolExecutor(max_workers=4) as executor:
            # Soumettre les requêtes en parallèle
            futures = [executor.submit(get, url) for url in urls]

            # Récupérer les résultats au fur et à mesure qu'ils sont prêts
            for future in as_completed(futures):
                try:
                    response = future.result()
                    results.append(response)
                except Exception as e:
                    print(f"Erreur lors de la requête : {e}")

        return results

    def fetch_data(self):
        """
        Récupère les données de l'API de manière asynchrone
        """
        urls = [self.__apilink + f"lines?size={self.maxlines}&start={i * self.maxlines}" for i in range(self.maxlines)]
        responses = self.make_requests(urls)

        # Fusionner les résultats de toutes les requêtes
        all_data = []
        for response in responses:
            all_data.extend(response.json()["results"])

        return all_data

    def filter_communes(self):
        """
        juste les communes
        """
        return sorted(set([com["raison_sociale"] for com in self.france if self.__is_commune(com)]))

    def filter_departements(self):
        """
        juste les départements
        """
        return sorted(set([dep["departement"] for dep in self.france]))

    def filter_regions(self):
        """
        juste les régions
        """
        return sorted(set([reg["region"] for reg in self.france]))

    def __is_commune(self, data):
        """
        Vérifier si les données représentent une commune pertinente
        """
        return ("type_de_collectivite" in data.keys() and "type_de_structure" in data.keys()
                and data["type_de_collectivite"] == "Communes"
                and data["type_de_structure"] == "Collectivité territoriale (dont EPCI)")