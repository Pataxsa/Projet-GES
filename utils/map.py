"""
Module map pour générer une carte
"""

from folium import TileLayer, Map as MAP, GeoJsonPopup, GeoJson, LayerControl
from json import load
from branca.colormap import LinearColormap
from os.path import isfile
from webbrowser import open as webopen

from utils.api import Api
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
        Fonction save qui sauvegarde la carte si le fichier existe et lance le fichier html
        """
        
        if not isfile("map.html"):
            self.__map.save(name)

        webopen(name)

    # Fonction privé qui permet de générer les données de la carte
    def __generate(self) -> None:
        TileLayer('cartodbpositron', name='GES').add_to(self.__map)

        for name, geojson in self.__geojson.items():
            data = self.__data.get(name, {})

            for feature in geojson["features"]:
                co2_value = data.get(feature['properties']['nom'])

                feature["properties"]["CO2"] = f"{int(co2_value):,} Tonnes" if co2_value is not None else "Pas de valeurs"

        self.__addGeoJson("Régions", True)
        self.__addGeoJson("Départements")

        LayerControl().add_to(self.__map)
    
    # Fonction privé qui permet l'ajout des données sur la carte (geojson et colormap)
    def __addGeoJson(self, name: str, show: bool = False) -> None:
        data = self.__data[name.replace("é","e")]
        geojson = self.__geojson[name.replace("é","e")]

        colormap = LinearColormap(["green", "yellow", "red"], vmin=min(data.values()), vmax=(sum(data.values())/len(data.values())))

        colormap.caption = f"Total CO2 en tonnes des {name.lower()}"
        self.__map.add_child(colormap)

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

    # Fonction privé qui permet de gérer les couleurs sur la carte
    def __usecolor(self, feature: FEATURE_TYPE, data: dict[str, int], colormap: LinearColormap) -> str:
        if feature["properties"]["nom"] in data:
            return colormap(data[feature["properties"]["nom"]])
        else:
            return "grey"
