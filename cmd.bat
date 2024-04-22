:: Programme pour faciliter les commandes dans l'environnement (faire ./cmd)

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

:: Initialisation de l'environnement si il n'existe pas
if not exist %DATAPATH%\%ENV_NAME% ( 
    echo Installation de l'environnement...
    call %PYTHON_PATH% -m venv %DATAPATH%\%ENV_NAME%

    call %DATAPATH%\%ENV_NAME%\Scripts\activate 

    py -m pip install --upgrade pip 

    pip install -r requirements.txt 
)

:loop
(
    call %DATAPATH%\%ENV_NAME%\Scripts\activate
    set /p command="PS (%ENV_NAME%) %CD%>"
)

if "%command%"=="exit" (
    exit /b
)

%command%
goto loop