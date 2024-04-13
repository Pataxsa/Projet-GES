:: Build.bat pour Windows

@echo off

set DATAPATH="%LocalAppData%\Projet-GES"
set ENV_NAME=env

:: Demande de réinstallation de l'environnement
if not %ERRORLEVEL% == 0 (
    :input
    set /p INPUT="Voulez vous reinstaller l'environnement ? (Y/N):"
    if "%INPUT%"=="Y" (
        goto install
    )
)

:: Initialisation de l'environnement si il n'existe pas
if not exist %DATAPATH%\%ENV_NAME% (
    :install
    echo Installation de l'environnement...
    py -m venv %DATAPATH%\%ENV_NAME%

    call %DATAPATH%\%ENV_NAME%\Scripts\activate 

    py -m pip install --upgrade pip 

    pip install -r requirements.txt 
) else (

    call %DATAPATH%\%ENV_NAME%\Scripts\activate

    :: Vérification et installation des dépendances dans l'environnement
    pip-sync requirements.txt
)


:: Reinstallation de l'environnement si il y a une erreur
if not %ERRORLEVEL% == 0 (
    goto input
)

set /p INPUT="Voulez vous compiler en mode portable ? (Y/N):"

:: Compilation du programme (mode portable ou non)
if "%INPUT%"=="Y" (
    pyinstaller specs/build-portable.spec
) else (
    pyinstaller specs/build.spec
)