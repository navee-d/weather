# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['new.py'],
    pathex=[],
    binaries=[],
    datas=[('1111at 20.56.53_16f9cdc6.jpg', '.'), ('next-buttonnavee.png', '.'), ('heavy-rain.png', '.'), ('cloudy.png', '.'), ('fog.png', '.'), ('haze.png', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='new',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
