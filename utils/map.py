"""
Module map pour générer une carte
"""

from folium import TileLayer, Map, GeoJsonPopup, GeoJson, LayerControl
from json import load
from branca.colormap import LinearColormap
from os.path import isfile
from utils.api import Api
import webbrowser


class MAP:
    """
    Classe MAP pour générer une carte en fonction des valeures CO2
    """

    # Initialisation (constructeur)
    def __init__(self, api:Api):
        # Api et Carte
        self.map = Map(location=[46.862725, 2.287592], zoom_start=6, tiles=None)
        self.api = api
        
        # Fichiers geojson des départements/regions
        self.geojson_departements = load(open(".\\data\\departements.geojson"))
        self.geojson_regions = load(open(".\\data\\regions.geojson"))

        # Co2 des departements/regions
        self.data_departements = self.api.getCO2Total("Départements")
        self.data_regions = self.api.getCO2Total("Régions")

        # Générer la carte (une fois car la carte ne changera jamais)
        self.__generate()

    def save(self, name:str):
        """
        Fonction save qui sauvegarde la carte si le fichier existe et lance le fichier html
        """
        
        if not isfile("map.html"):
            self.map.save(name)

        webbrowser.open(name)

    # Fonction privé qui permet de générer les données de la carte
    def __generate(self):
        TileLayer('cartodbpositron', name='GES').add_to(self.map)

        for prm in self.geojson_regions["features"]:
            prm["properties"].update({ "CO2": f"{int(self.data_regions[prm["properties"]["nom"]])} Tonnes" if (prm["properties"]["nom"] in self.data_regions) else "Pas de valeurs" })

        for prm in self.geojson_departements["features"]:
            prm["properties"].update({ "CO2": f"{int(self.data_departements[prm["properties"]["nom"]])} Tonnes" if (prm["properties"]["nom"] in self.data_departements) else "Pas de valeurs" })

        self.__addGeoJson("Régions", self.data_regions, self.geojson_regions, True)
        self.__addGeoJson("Départements", self.data_departements, self.geojson_departements)

        LayerControl().add_to(self.map)
    
    # Fonction privé qui permet l'ajout des données sur la carte (geojson et colormap)
    def __addGeoJson(self, name:str, data:dict, geojson:dict, show:bool = False):
        colormap = LinearColormap(["green", "yellow", "red"], vmin=min(data.values()), vmax=(sum(data.values())/len(data.values())))

        colormap.caption = f"Total CO2 en tonnes des {name.lower()}"
        self.map.add_child(colormap)

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
        ).add_to(self.map)

    # Fonction privé qui permet de gérer les couleurs sur la carte
    def __usecolor(self, feature, data, colormap):
        if feature["properties"]["nom"] in data.keys():
            return colormap(data[feature["properties"]["nom"]])
        else:
            return "grey"
