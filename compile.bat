:: Compile.bat pour Windows

@echo off

set DATAPATH="%LocalAppData%\Projet-GES"
set ENV_NAME=env

:: Initialisation de l'environnement si il n'existe pas
IF NOT EXIST %DATAPATH%\%ENV_NAME% ( 
    py -m venv %DATAPATH%\%ENV_NAME%

    call %DATAPATH%\%ENV_NAME%\Scripts\activate 

    py -m pip install --upgrade pip 
    pip install setuptools

    pip install -r requirements.txt 
) ELSE (

    call %DATAPATH%\%ENV_NAME%\Scripts\activate

    :: Vérification et installation des dépendances dans l'environnement
    py -c "import pkg_resources; pkg_resources.require(open('requirements.txt',mode='r'))" 2>NUL || pip install -r requirements.txt
)

(
    :: Compilation du programme
    pyinstaller -F --noconsole --onefile --add-data "interface;interface" --add-data "data/*.geojson;data" --icon="interface/icons/icon-x64.ico" --name="Projet-GES" --version-file="version.txt" main.py
)