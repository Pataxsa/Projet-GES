#!/bin/bash
# Launch.bash pour Linux

DATAPATH="$HOME/Projet-GES/"
ENV_NAME="env"

# Initialisation de l'environnement si il n'existe pas
if [ ! -d $DATAPATH$ENV_NAME ]
then
    echo "Installation de l'environnement..."

    python3 -m venv $DATAPATH$ENV_NAME

    chmod u+x $DATAPATH$ENV_NAME/bin/activate
    source $DATAPATH$ENV_NAME/bin/activate 

    python3 -m pip install --upgrade pip 

    pip3 install -r requirements.txt
else
    source $DATAPATH$ENV_NAME/bin/activate

    # Vérification et installation des dépendances dans l'environnement
    pip-sync requirements.txt
fi

# Lancement du programme
python3 main.py