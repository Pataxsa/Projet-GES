from subprocess import check_call, DEVNULL
from sys import executable

#Installe les librairies si elles n'existent pas
def checkLibs():
    try:
        import requests
        import matplotlib
    except ModuleNotFoundError as e:
        check_call([executable, '-m', 'pip', 'install', e.name], stdout=DEVNULL)
