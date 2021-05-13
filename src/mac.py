import globals
from pathlib import Path

possibleLocations = ["/Applications/TeamSpeak.app/Contents/Resources/html/client_ui/index.html"]

def searchForInstallation():
    for x in possibleLocations:
        try:
            if Path(x).is_file():
                return x
        except: pass
    return ""

def initPlatform():
    globals.platformHome = "~"
    globals.platform = globals.Platform.Mac
    globals.filetype = ".html"
    globals.filetypeString = "Please select index.html"
    globals.filename = searchForInstallation()
