"""
Module main pour créer et lancer l'interface
"""
from PySide6.QtWidgets import QApplication

from app.windows.preload import Preload

if __name__ == "__main__":
    app = QApplication()

    preload_window = Preload() # Préchargement (splash_screen)
    preload_window.update(text="Importation des modules...", percent=40)

    from app.windows.main import Main

    preload_window.update(text="Chargement de l'interface...", percent=70)
    main_window = Main(title="Emissions de GES par types de localités") # Menu principal
    preload_window.update(text="Affichage de l'interface...", percent=100)
    main_window.show()

    preload_window.deleteLater()
    
    app.exec()
