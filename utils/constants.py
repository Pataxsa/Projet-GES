"""
Module constants pour les constantes utilitaires
"""

import sys

# Base du chemin pour les ressources
RESOURCE_PATH: str = getattr(sys, '_MEIPASS', ".")

# Base du lien API
API_LINK: str = "https://data.ademe.fr/data-fair/api/v1/datasets/bilan-ges/"
