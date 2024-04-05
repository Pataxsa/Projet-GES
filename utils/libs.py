from subprocess import run, CalledProcessError

def checkLibs():
    modules = ['folium','branca','requests','matplotlib','customtkinter']
    possession = run(["py", "-m", "pip", "list"], capture_output=True, text=True).stdout.split()
    possession = [possession[i] for i in range(0,len(possession),2)]

    for i in modules:
        if not i in possession:
            try:
                if i == "customtkinter":
                    # Customtkinter ne s'installe pas avec poetry (jsp pk)
                    print("Installation de " + i)
                    run(["py", "-m", "pip", "install", "customtkinter"])
                    break

                print("Installation des packages avec poetry...")
                run(["py", "-m", "pip","install","poetry"])
                run(["py", "-m", "poetry","install"])

                print("Poetry a été installé avec succès!")
                break

            except CalledProcessError as e:
                print(f"Une erreur s'est produite lors de l'installation de Poetry : {e}")
                break