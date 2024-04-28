import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl
from utils.local_serveur import LocalServer
from utils.map import MAP
from utils.api import Api
"""
class Test(QMainWindow):
    def __init__(self, titre):
        super().__init__()
        self.setWindowTitle(titre)
        self.setGeometry(100, 100, 800, 600)

    def closeEvent(self, event):
        self.local_server.stop_server()
        event.accept()

    def init(titre_app):
        app = QApplication(sys.argv)
        window = Test(titre=titre_app)
        window.local_server = LocalServer(directory=".")
        window.local_server.start_server()
        web_view = QWebEngineView(window)
        web_view.load(QUrl("http://localhost:8000/../map.html"))
        window.setCentralWidget(web_view)
        window.show()
        sys.exit(app.exec_())


Test.init("intégration de la carte")
"""