<p align="center"><img src="icon.png" width="128" alt="Icona Estrai P7M"></p>

# Estrai P7M

Applicazione desktop (macOS / Windows) per estrarre i documenti originali dai file firmati digitalmente in formato **CAdES `.p7m`** (es. fatture elettroniche, atti firmati).

Non richiede OpenSSL né altri tool esterni: l'estrazione avviene in Python puro tramite [asn1crypto](https://github.com/wbond/asn1crypto).

## Funzionalità

- **Cartella (ricorsivo):** cerca ed estrae tutti i `.p7m` in una cartella e nelle sottocartelle
- **Singolo file:** estrae un solo `.p7m`
- Gestione dei file **firmati più volte** (`doc.pdf.p7m.p7m` → `doc.pdf.p7m` → `doc.pdf`)
- Opzione per sovrascrivere o saltare i file già estratti
- Log colorato con riepilogo di estratti, saltati ed errori

## Requisiti

- Python 3.9+ con Tkinter
- `asn1crypto`

```bash
pip install asn1crypto
```

## Uso

```bash
python3 estrai_p7m.py
```

Il file estratto viene salvato nella stessa cartella del `.p7m`, con il nome senza l'estensione `.p7m`.

## Creare l'app

Con [PyInstaller](https://pyinstaller.org/):

```bash
pip install pyinstaller
pyinstaller EstraiP7M.spec
```

L'app viene generata in `dist/EstraiP7M.app`.

In alternativa con py2app (solo macOS):

```bash
pip install py2app
python3 setup.py py2app
```

Per rigenerare l'icona (`EstraiP7M.icns`, richiede Pillow e macOS):

```bash
pip install pillow
python3 make_icon.py
```

## Autore

Ing. Carmine Palermo — [www.pcwebagency.it](https://www.pcwebagency.it)

## Licenza

[MIT](LICENSE)
