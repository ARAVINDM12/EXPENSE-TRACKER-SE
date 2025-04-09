# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:\\ARAVIND\\PROJECT\\SE\\EXPENSE-TRACKER-SE\\ExpenseApp\\splash.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\ARAVIND\\PROJECT\\SE\\EXPENSE-TRACKER-SE\\ExpenseApp\\Images\\SS.png', 'Images'), ('C:\\ARAVIND\\PROJECT\\SE\\EXPENSE-TRACKER-SE\\expenses.db', '.')],
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
    [],
    exclude_binaries=True,
    name='splash',
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
    icon=['C:\\ARAVIND\\PROJECT\\SE\\EXPENSE-TRACKER-SE\\ExpenseApp\\SS.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='splash',
)
