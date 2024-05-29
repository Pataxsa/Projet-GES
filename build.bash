#!/bin/bash
# build.bash pour Linux

echo "Onefile ?: YES/NO"

read resp

# Compilation du programme
if [ $resp == "YES" ]; then
    python setup.py bdist_appimage
else
    python setup.py build
fi