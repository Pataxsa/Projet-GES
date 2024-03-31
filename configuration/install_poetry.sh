#!/bin/bash
#installer poetry sinon c'est compliqué
curl -sSL https://install.python-poetry.org | python -

#doit d'exécution pour lancer le script
chmod +x install_poetry.sh

#installation des dépendances
poetry install
