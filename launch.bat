:: Launch.bat pour Windows

@echo off

set DATAPATH="%LocalAppData%\Projet-GES"
set ENV_NAME=env

:: Initialisation de l'environnement si il n'existe pas
IF NOT EXIST %DATAPATH%\%ENV_NAME% ( 
    :install
    echo Installation de l'environnement...
    py -m venv %DATAPATH%\%ENV_NAME% 

    call %DATAPATH%\%ENV_NAME%\Scripts\activate

    py -m pip install --upgrade pip 

    pip install -r requirements.txt
) ELSE (

    call %DATAPATH%\%ENV_NAME%\Scripts\activate

    :: Vérification et installation des dépendances dans l'environnement
    pip-sync requirements.txt
)

(
    :: Reinstallation de l'environnement si il y a une erreur
    if NOT %ERRORLEVEL% == 0 (
        goto install
    )
    :: Lancement du programme
    py main.py
)