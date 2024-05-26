:: Build.bat pour Windows

@echo off

set "DATAPATH=%LocalAppData%\Projet-GES"
set ENV_NAME=env
set "BASE_PYTHON_PATH=%LocalAppData%\Programs\Python"
set PYTHON_PATH=Nul

:: Utilisation du chemin absolu vers python
for /D %%A in ("%BASE_PYTHON_PATH%\*") do (
    echo %%~nxA | find /I "Python" > Nul && (
        set PYTHON_PATH=%%A
    )
)

if %PYTHON_PATH% == Nul (
    echo Je n'ai trouve aucune installation de python :^(
    echo Si vous n'avez pas installe python 3.X ^(3.12 par exemple^)
    echo Voici le chemin dans lequel python doit normalement s'installer %BASE_PYTHON_PATH%\Python[version]
    pause
    exit 2
)

set "PYTHON_PATH=%PYTHON_PATH%\python.exe"

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
    call %PYTHON_PATH% -m venv %DATAPATH%\%ENV_NAME%

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

set /p INPUT="Voulez vous compiler en mode installateur ? (Y/N):"

:: Compilation du programme (mode installateur ou non)
if "%INPUT%"=="Y" (
    py setup.py bdist_msi
) else (
    py setup.py build
)