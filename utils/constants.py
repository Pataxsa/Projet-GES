"""
Module constants pour les constantes utilitaires
"""

import sys

"""
Constantes
"""

# Chemin ROOT
ROOT_PATH: str = getattr(sys, '_MEIPASS', ".")

# Chemin vers les ressources (assets)
RESOURCE_PATH: str = f"{ROOT_PATH}\\app\\assets"

# Base du lien API
API_LINK: str = "https://data.ademe.fr/data-fair/api/v1/datasets/bilan-ges/"

"""
Constantes type alias
"""

# Type GeoJson
type GEO_JSON_TYPE = dict[str, str | list[dict[str, str | dict[str, str | int | list[list[float, float]]]]]]