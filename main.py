"""
Module main pour créer et lancer l'interface
"""

from PySide6.QtWidgets import QApplication
import sys
from app.windows.preload import Preload
from app.windows.main import Main

if __name__ == "__main__":
    app = QApplication(sys.argv)

    preload_window = Preload() # Préchargement (splash_screen)

    preload_window.update(text="Chargement de l'interface...", percent=50)
    window = Main(title = "Projet-GES")
    
    window.play_sound()
    preload_window.update(text="Affichage de l'interface...", percent=100)
    window.show()

    preload_window.deleteLater()
    sys.exit(app.exec())
