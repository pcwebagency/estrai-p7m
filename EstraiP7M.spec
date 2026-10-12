# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['estrai_p7m.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['asn1crypto', 'asn1crypto.cms', 'asn1crypto.core', 'asn1crypto.algos', 'asn1crypto.x509', 'asn1crypto.keys'],
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
    name='EstraiP7M',
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
    icon=['EstraiP7M.icns'],
)
app = BUNDLE(
    exe,
    name='EstraiP7M.app',
    icon='EstraiP7M.icns',
    bundle_identifier=None,
)
