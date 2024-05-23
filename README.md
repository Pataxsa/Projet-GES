<div align="center">
    <img src="https://gitlab.univ-lr.fr/uploads/-/system/project/avatar/9036/icon.ico?width=96" width="134" height="134">
    <h1>Projet-GES</h1>
</div>

# 📗 Table des matières
- [📖 A propos du projet](#à-propos)
  - [🚀 Exemple de lancement](#exemple)
  - [🛠 Dépendances](#modules)
- [💻 Pour commencer](#pour-commencer)
  - [🐍 Compatibilité](#compatibilité)
  - [🏗️ Installation](#installation)
  - [🚗 Installation rapide](#installation-rapide)
  - [⚙️ Configuration](#configuration)
- [🛣️ Roadmap](#roadmap)
- [👥 Auteurs](#auteurs)
- [👷‍♂️ Superviseurs](#superviseurs)

# À propos
<h4>Projet-GES est un projet construit avec python qui permet d'afficher des graphiques montrant l'évolution de gaz a effet de serre dans un lieu. Vous pourrez y trouver une carte et générer des graphiques montrant les émissions de gaz à effet de serre en France et dans les territoires français.</h4>

  ### Exemple
  <div align="center">
      <img src="exemple_lancement.gif"></img>
  </div>

  ### Modules
  - Pour réaliser ce projet nous avons utilisé majoritairement les modules suivants :
    - <a href="https://pypi.org/project/PySide6/">🖥️ Pyside6 </a>
    - <a href="https://matplotlib.org/stable/index.html">📈 Matplotlib</a>
    - <a href="https://pypi.org/project/folium/">🌍 Folium</a>

# Pour commencer
  - ## Compatibilité
    - Avant de commencer vérifiez que votre python soit compatible avec le projet : 
      | Version  | Compatibilité |
      | --------------- | ----------- | 
      | >=3.10 | ✅ |
      | <3.10, >3.8 | 🤷 |
      | <=3.8  | ❌ |

  - ## Installation
    1. Tout d'abord utilisez cette commande git afin de télécharger le projet
        ```bash
        git clone https://gitlab.univ-lr.fr/l12024/lescrazy/Projet-GES.git
        ```

    2. Puis pour installer les modules entrez la commande suivante dans votre terminal
        ```bash 
        pip install -r requirements.txt # Windows
        pip3 install -r requirements.txt # Linux
        ```

    3. Et enfin pour lancer le projet vous pouvez exécuter cette commande dans le terminal à partir de la racine du projet
        ```bash
        python main.py # Windows
        python3 main.py # Linux
        ```

  - ## Installation rapide
    - Pour installer le projet plus rapidement, vous pouvez aussi utiliser le fichier [launch.bat](launch.bat) sur windows ou [launch.sh](launch.sh) si vous êtes sur un système d'exploitation Linux
      ```bash 
      ./launch.bat # Windows

      # Linux
      chmod u+x launch.sh
      ./launch.sh
      ```

  - ## Configuration
    - Si vous le voulez, vous pouvez aussi modifier la configuration du projet dans le fichier [constants](utils/constants.py)
      ```python
      # Chemin ROOT
      ROOT_PATH: str = getattr(sys, '_MEIPASS', ".")

      # Chemin vers les ressources (assets)
      RESOURCE_PATH: str = f"{ROOT_PATH}\\app\\assets"

      # Base du lien API
      API_LINK: str = "https://data.ademe.fr/data-fair/api/v1/datasets/bilan-ges/"

      # Expiration en seconde du cache des requetes (1H par defaut)
      REQUEST_CACHE_EXPIRE: int = 60*60
      ```

# Roadmap
- [x] Ajout d'une interface
- [x] Optimisation du temps de lancement
- [ ] Ajout d'une page paramètres
- [ ] Ajout de fonctionalité de tri
- [ ] Ajout d'un système multi-language

# Auteurs

| <a href="https://gitlab.univ-lr.fr/nchamoua"> <img src="https://gitlab.univ-lr.fr/uploads/-/system/user/avatar/2426/avatar.png?width=800" width="64" height="64"> </a> | **Nom :** Noam Chamouard <br> **GitLab :** [mon profil](https://gitlab.univ-lr.fr/nchamoua) |
|:----------------------------------------------------------------------------------------------------------------------------------:|:----------------------------------------------------------------------------------------------------:|

| <a href="https://gitlab.univ-lr.fr/acvjetic"> <img src="https://gitlab.univ-lr.fr/uploads/-/system/user/avatar/2468/avatar.png?width=800" width="64" height="64"> </a> | **Nom :** Axel Cvjetic <br> **GitLab :** [mon profil](https://gitlab.univ-lr.fr/acvjetic) |
|:---------------------------------------------------------------------------------------------------------------------------------:|:----------------------------------------------------------------------------------------------------:|

| <a href="https://gitlab.univ-lr.fr/dollivie"> <img src="https://secure.gravatar.com/avatar/a261e03fb78a7abdec058954aafcc0778fc8cd77f580cebced9ba173f95d91ed?s=64&d=identicon" width="64" height="64"> </a> | **Nom :** Dimitri Ollivier <br> **GitLab :** [mon profil](https://gitlab.univ-lr.fr/dollivie) |
|:----------------------------------------------------------------------------------------------------------------------------------:|:----------------------------------------------------------------------------------------------------:|

| <a href="https://gitlab.univ-lr.fr/imugisha"> <img src="https://secure.gravatar.com/avatar/a651d3b5f3a9f490d36e163332be73cc24f1047f28735b4e9f788b3637bb9c43?s=64&d=identicon" width="64" height="64"> </a> | **Nom :** Iyanchrist Mugisha <br> **GitLab :** [mon profil](https://gitlab.univ-lr.fr/imugisha) |
|:----------------------------------------------------------------------------------------------------------------------------------:|:----------------------------------------------------------------------------------------------------:|

# Superviseurs

| <a href="https://gitlab.univ-lr.fr/jviaud"> <img src="https://gitlab.univ-lr.fr/uploads/-/system/user/avatar/566/avatar.png?width=800" width="64" height="64"> </a> | **Nom :** Jean-François Viaud <br> **GitLab :** [mon profil](https://gitlab.univ-lr.fr/jviaud) |
|:----------------------------------------------------------------------------------------------------------------------------------:|:----------------------------------------------------------------------------------------------------:|