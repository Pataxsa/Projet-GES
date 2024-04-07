:: Launch.bat pour Windows

:: Vérification et installation des dépendances
py -c "import pkg_resources; pkg_resources.require(open('requirements.txt',mode='r'))" 2>NUL || py -m pip install -r requirements.txt

:: Lancement du programme
py main.py