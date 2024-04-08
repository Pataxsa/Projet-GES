# Compile.sh pour Linux

DATAPATH="$HOME\\Projet-GES\\"
ENV_NAME="env"

# Initialisation de l'environnement si il n'existe pas
if [ ! -f $DATAPATH\\$ENV_NAME ]
then
    python3 -m venv $DATAPATH\\$ENV_NAME

    $DATAPATH\\$ENV_NAME\bin\activate 

    python3 -m pip install --upgrade pip 
    pip3 install setuptools

    pip3 install -r requirements.txt 
else
    $DATAPATH\\$ENV_NAME\bin\activate

    # Vérification et installation des dépendances dans l'environnement
    python3 -c "import pkg_resources; pkg_resources.require(open('requirements.txt',mode='r'))" &>/dev/null || pip3 install -r requirements.txt

# Compilation du programme
pyinstaller -F --noconsole --onefile --add-data "interface;interface" --add-data "data/*.geojson;data" main.py