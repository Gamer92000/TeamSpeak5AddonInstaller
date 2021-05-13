pyinstaller --onefile --hidden-import=PIL._tkinter_finder -w -n TS5AddonInstaller_Mac -y src/main.py
(cd dist; zip -r TS5AddonInstaller_Mac.zip TS5AddonInstaller_Mac.app)
rm -rf dist/TS5AddonInstaller_Mac.app
rm dist/TS5AddonInstaller_Mac
