# -*- mode: python ; coding: utf-8 -*-
# Fichier utilisé pour build le fichier en exe (version non portable)
# Transformer les fichiers en setup (avec InstallForge par exemple: https://installforge.net/)


a = Analysis(
    ['../main.py'],
    pathex=[],
    binaries=[],
    datas=[('../interface', 'interface'), ('../data', 'data')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Projet-GES',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version='version.txt',
    icon=['../interface/icons/icon-x64.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Projet-GES',
)