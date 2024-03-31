#!/bin/bash
#installer poetry sinon c'est compliqué
pip install poetry

#doit d'exécution pour lancer le script
chmod +x .

#installation des dépendances
poetry install
