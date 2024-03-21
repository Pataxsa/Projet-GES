"""
Module map pour générer une carte
"""

from folium import TileLayer, Map, GeoJsonPopup, GeoJson, LayerControl
from json import load
from branca.colormap import LinearColormap
from utils.api import Api
import webbrowser

class MAP:
    """
    Classe MAP pour générer une carte en fonction des valeures CO2
    """

    #Initialisation (constructeur)
    def __init__(self, api:Api):
        self.map = None
        self.geojson_departements = load(open("./data/departements.geojson"))
        self.geojson_regions = load(open("./data/regions.geojson"))
        self.api = api
        self.generated = False
    
    def generate(self):
        """
        Crée la carte
        """

        self.map = Map(location=[46.862725,2.287592], zoom_start=6, tiles = None)
        TileLayer('cartodbpositron', name='GES').add_to(self.map)

        #Lent: non optimisé
        data_departements = self.api.getCO2Total("Départements")
        data_regions = self.api.getCO2Total("Régions")


        colormap_regions = LinearColormap(["green", "yellow", "red"], vmin=min(data_regions.values()), vmax=max(data_regions.values()))

        colormap_regions.caption = "Total CO2 en tonnes des régions"
        self.map.add_child(colormap_regions)

        popup = GeoJsonPopup(fields=["nom"], labels=False)

        GeoJson(
            data=self.geojson_regions,
            name="Regions",
            style_function=lambda feature: {
                "fillColor": self.__check(feature, data_regions, colormap_regions),
                "color": "black",
                "weight": 2
            },
            fill_opacity=0.7,
            line_opacity=0.2,
            popup=popup,
            popup_keep_highlighted=True,
            highlight_function=lambda feature: {
                "fillColor": (
                    "blue"
                ),
            },
        ).add_to(self.map)


        colormap_departements = LinearColormap(["green", "yellow", "red"], vmin=min(data_departements.values()), vmax=max(data_departements.values()))

        colormap_departements.caption = "Total CO2 en tonnes des départements"
        self.map.add_child(colormap_departements)

        popup2 = GeoJsonPopup(fields=["nom"], labels=False)

        GeoJson(
            show=False,
            data=self.geojson_departements,
            name="Departements",
            style_function=lambda feature: {
                "fillColor": self.__check(feature, data_departements, colormap_departements),
                "color": "black",
                "weight": 2
            },
            fill_opacity=0.7,
            line_opacity=0.2,
            popup=popup2,
            popup_keep_highlighted=True,
            highlight_function=lambda feature: {
                "fillColor": (
                    "blue"
                ),
            },
        ).add_to(self.map)

        LayerControl().add_to(self.map)

        self.generated = True

    def save(self, name:str):
        """
        Sauveguarde la carte et lance le fichier html
        """

        if self.generated:
            self.map.save(name)
            webbrowser.open(name)
    

    def __check(self, feature, data, colormap):
        if feature["properties"]["nom"] in data.keys():
            return colormap(data[feature["properties"]["nom"]])
        else:
            return "grey"