from cx_Freeze import setup, Executable
from utils.constants import RESOURCE_PATH, APP_NAME, APP_DESCRIPTION, APP_VERSION, AUTHOR

options = {
    "build_exe": {
        "excludes": ["fontTools"],
        "zip_include_packages": ["encodings", "PySide6", "shiboken6", "matplotlib", "numpy", "PIL"],
        "include_files": [("./app/assets", "app/assets"), ("./data", "data"), "./LICENCE.txt"],
        "optimize": 1
    },
    "bdist_msi": {
        'add_to_path': False, 
        'initial_target_dir': f"[LocalAppDataFolder]\\Programs\\{APP_NAME}",
        'all_users': True,
        'install_icon': f"{RESOURCE_PATH}\\icons\\icon-x32.ico"
    }
}

executable = Executable(
    script="main.py",
    base="gui",
    target_name=APP_NAME,
    icon=f"{RESOURCE_PATH}\\icons\\icon-x64.ico",
    shortcut_name=APP_NAME,
    shortcut_dir="DesktopFolder"
)

setup(
    name=APP_NAME,
    version=APP_VERSION,
    description=APP_DESCRIPTION,
    author=AUTHOR,
    options=options,
    executables=[executable]
)