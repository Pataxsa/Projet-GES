# Build.sh pour Linux
# TODO: a mettre a jour plus tard

DATAPATH="$HOME\\Projet-GES\\"
ENV_NAME="env"

# Initialisation de l'environnement si il n'existe pas
if [ ! -f $DATAPATH\\$ENV_NAME ]
then
    echo "Installation de l'environnement..."
    python3 -m venv $DATAPATH\\$ENV_NAME

    $DATAPATH\\$ENV_NAME\bin\activate 

    python3 -m pip install --upgrade pip 

    pip3 install -r requirements.txt 
else
    $DATAPATH\\$ENV_NAME\bin\activate

    # Vérification et installation des dépendances dans l'environnement
    pip-sync requirements.txt

# Compilation du programme
pyinstaller specs/build-portable.spec