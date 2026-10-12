from setuptools import setup

APP = ['estrai_p7m.py']
OPTIONS = {
    'argv_emulation': False,
    'iconfile': 'EstraiP7M.icns',
    'plist': {
        'CFBundleName': 'Estrai P7M',
        'CFBundleDisplayName': 'Estrai P7M',
        'CFBundleIdentifier': 'it.pcwebagency.estraip7m',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0',
        'NSHumanReadableCopyright': '© 2026 Ing. Carmine Palermo',
        'NSHighResolutionCapable': True,
    },
    'packages': [],
}

setup(
    app=APP,
    name='Estrai P7M',
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
