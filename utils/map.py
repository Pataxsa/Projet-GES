"""
Module map pour générer une carte
"""

from folium import TileLayer, Map as MAP, GeoJsonPopup, GeoJson, LayerControl
from json import load
from branca.colormap import LinearColormap
from os.path import isfile
from utils.api import Api
from utils.constants import ROOT_PATH, GEO_JSON_TYPE
from webbrowser import open as webopen

class Map:
    """
    Classe MAP pour générer une carte en fonction des valeures CO2
    """

    # Initialisation (constructeur)
    def __init__(self, api: Api) -> None:
        # Carte
        self.__map: MAP = MAP(location=[46.862725, 2.287592], zoom_start=6, tiles=None)
        
        # Fichiers geojson des départements/regions
        self.__geojson_departements: GEO_JSON_TYPE = load(open(f"{ROOT_PATH}\\data\\departements.geojson"))
        self.__geojson_regions: GEO_JSON_TYPE = load(open(f"{ROOT_PATH}\\data\\regions.geojson"))

        # Co2 des departements/regions
        self.__data_departements: dict[str, int] = api.getCO2Total("Départements")
        self.__data_regions: dict[str, int] = api.getCO2Total("Régions")

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

        for prm in self.__geojson_regions["features"]:
            prm["properties"].update({ "CO2": f"{int(self.__data_regions[prm['properties']['nom']]):,} Tonnes" if (prm['properties']['nom'] in self.__data_regions) else "Pas de valeurs" })

        for prm in self.__geojson_departements["features"]:
            prm["properties"].update({ "CO2": f"{int(self.__data_departements[prm['properties']['nom']]):,} Tonnes" if (prm['properties']['nom'] in self.__data_departements) else "Pas de valeurs" })


        self.__addGeoJson("Régions", self.__data_regions, self.__geojson_regions, True)
        self.__addGeoJson("Départements", self.__data_departements, self.__geojson_departements)

        LayerControl().add_to(self.__map)
    
    # Fonction privé qui permet l'ajout des données sur la carte (geojson et colormap)
    def __addGeoJson(self, name: str, data: dict[str, int], geojson: dict[str, str | list[dict[str, str | dict[str, str | int | list[list[float, float]]]]]], show: bool = False) -> None:
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
    def __usecolor(self, feature: dict[str, str | dict[str, str | int | list[list[float, float]]]], data: dict[str, int], colormap: LinearColormap) -> str:
        if feature["properties"]["nom"] in data.keys():
            return colormap(data[feature["properties"]["nom"]])
        else:
            return "grey"
