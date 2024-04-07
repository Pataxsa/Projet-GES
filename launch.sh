# Launch.sh pour Linux

# Vérification et installation des dépendances
python3 -c "import pkg_resources; pkg_resources.require(open('requirements.txt',mode='r'))" &>/dev/null || pip3 install -r requirements.txt

# Lancement du programme
python3 main.py