"""
Module main pour créer et lancer l'interface
"""

from sys import version_info

def check_version(major: int = 3, minor: int = 10) -> bool:
    return version_info.major >= major and version_info.minor >= minor

if not check_version(3, 10):
    print(f"Votre version {version_info.major}.{version_info.minor} de python est incompatible")
    exit()

from PySide6.QtWidgets import QApplication
from PySide6.QtWebEngineCore import QWebEngineSettings # Précharger le module sinon l'app ne se lance pas (on ne peut pas le mettre après le QApplication)

from app.windows.preload import Preload

if __name__ == "__main__":
    app = QApplication()

    preload_window = Preload(text="Importation des modules...", percent=40) # Préchargement (splash_screen)
    app.processEvents()

    from app.windows.main import Main

    preload_window.update(text="Chargement de l'interface...", percent=70)
    main_window = Main(title="Emissions de GES par types de localités") # Menu principal
    preload_window.update(text="Affichage de l'interface...", percent=100)
    main_window.show()

    preload_window.close()
    preload_window.deleteLater()
    
    app.exec()
