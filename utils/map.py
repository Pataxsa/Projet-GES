"""
Module map pour générer une carte

Modules :
    > folium.TileLayer : Pour ajouter des couches de tuiles (Départements - Régions)
    > folium.Map : Classe principale pour créer les objets de la map
    > folium.GeoJsonPopup : Pour afficher les données quand on clique sur une zone
    > folium.GeoJson : Pour ajouter des données en format GeoJson
    > folium.LayerControl : Pour pouvoir passer de Départements à Régions sur la map (controle des couches)

    > json.load`: Pour charger des données en .JSON
    > branca.colormap.LinearColormap : Pour créer des colormaps linéaires pour la visualisation des données
    > os.path.isdir et os.path.isfile : Pour vérifier si les fichiers / dossiers existent
    > os.mkdir et os.remove : Pour créer des dossiers et supprimer des fichiers

    > Api : import de la classe API pour obtenir les données CO2
    > GEO_JSON_TYPE et FEATURE_TYPE : Format / type de données à traiter
"""

from folium import TileLayer, Map as MAP, GeoJsonPopup, GeoJson, LayerControl
from json import load
from branca.colormap import LinearColormap
from os.path import isdir, isfile
from os import mkdir, remove

from utils import Api
from utils.constants import ROOT_PATH, GEO_JSON_TYPE, FEATURE_TYPE

class Map:
    """
    Classe MAP pour générer une carte en fonction des valeures CO2
    """

    # Initialisation (constructeur)
    def __init__(self, api: Api) -> None:
        # Carte
        self.__map: MAP = MAP(location=[46.862725, 2.287592], zoom_start=6, tiles=None)
        
        # Fichiers geojson des départements/regions
        geojson_departements: GEO_JSON_TYPE = load(open(f"{ROOT_PATH}\\data\\departements.geojson"))
        geojson_regions: GEO_JSON_TYPE = load(open(f"{ROOT_PATH}\\data\\regions.geojson"))
        self.__geojson: dict[str, GEO_JSON_TYPE] = {"Departements": geojson_departements, "Regions": geojson_regions}

        # Co2 des departements/regions
        data_departements: dict[str, int] = api.getCO2Total("Départements")
        data_regions: dict[str, int] = api.getCO2Total("Régions")
        self.__data: dict[str, dict[str, int]] = {"Departements": data_departements, "Regions": data_regions}

        # Générer la carte (une fois car la carte ne changera jamais)
        self.__generate()

    def save(self, name: str) -> None:
        """
        Fonction save qui sauvegarde la carte si le fichier existe

        Paramètres :
            > name (str) : nom du ficher quand il sera sauvegarder
        
        Return : None
        """

        if not isdir(f"{ROOT_PATH}\\tmp"):
            mkdir(f"{ROOT_PATH}\\tmp")
        
        self.__map.save(name)
    
    def delete(self, name: str) -> None:
        """
        Fonction delete qui supprime la carte si le fichier existe

        Paramètres : 
            > name (str) : nom à vérifier avant suppression

        Return : None
        """

        if isfile(name):
            remove(name)

    def __generate(self) -> None:
        """
        Fonction privé qui permet de générer les données de la carte
        
        Return : None
        """
        # Ajout de la première couche de la map
        TileLayer('cartodbpositron', name='GES').add_to(self.__map)

        # Ajout des données à chaque lieu
        for name, geojson in self.__geojson.items():
            data = self.__data[name]

            for feature in geojson["features"]:
                co2_value = data.get(feature['properties']['nom'])

                feature["properties"]["CO2"] = f"{int(co2_value):,} Tonnes" if co2_value is not None else "Pas de valeurs"

        # Ajout des couches, Régions par défaut
        self.__addGeoJson("Régions", True)
        self.__addGeoJson("Départements")

        # Bouton pour basculer d'une couche à une autre
        LayerControl().add_to(self.__map)

    def __addGeoJson(self, name: str, show: bool = False) -> None:
        """
        Fonction privé qui permet l'ajout des données sur la carte (geojson et colormap)
        
        Paramètres :
            name (str) : Le nom dess données GeoJSON à ajouter à la map
            show (bool) : True si les données sont visibles par défaut

        Return : None
        """

        data = self.__data[name.replace("é","e")]
        geojson = self.__geojson[name.replace("é","e")]

        # Définition variations de couleurs 
        colormap = LinearColormap(["green", "yellow", "red"], vmin=min(data.values()), vmax=(sum(data.values())/len(data.values())))

        # Ajout de la légende
        colormap.caption = f"Total CO2 en tonnes des {name.lower()}"
        self.__map.add_child(colormap)

        # Pop up lorsque l'on clique sur une zone
        popup = GeoJsonPopup(fields=["nom", "CO2"])

        GeoJson(
            show=show,
            data=geojson,
            name=name,
            style_function=lambda feature: {
                "fillColor": self.__usecolor(feature, data, colormap),
                "color": "black",
                "weight": 2
            },
            fill_opacity=0.7,
            line_opacity=0.2,
            popup=popup,
            popup_keep_highlighted=True,
            highlight_function=lambda feature: {
                "fillColor": "blue",
            },
        ).add_to(self.__map)

    def __usecolor(self, feature: FEATURE_TYPE, data: dict[str, int], colormap: LinearColormap) -> str:
        """    
        Fonction privé qui permet de gérer les couleurs sur la carte

        Paramètres :
            > feature (FEATURE_TYPE) : Lieu où placer la couleur
            > data (dict[str, int]) : Dictionnaire avec les valeurs de CO2 et les noms des lieux
            > colormap (LinearColormap) : Légende de couleur des valeurs CO2

        Return : (str) Couleur de remplissage
        """
        if feature["properties"]["nom"] in data:
            return colormap(data[feature["properties"]["nom"]])
        else:
            return "grey"
