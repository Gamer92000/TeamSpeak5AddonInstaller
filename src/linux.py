import globals
from pathlib import Path
from os.path import expanduser

# I'm happy to add more locations here, if they are reasonable.
possibleLocations = [expanduser("~/Programs/TeamSpeak/html/client_ui/index.html"),\
                     expanduser("~/.local/share/TeamSpeak/html/client_ui/index.html"),\
                     "/opt/TeamSpeak/html/client_ui/index.html"]

def searchForInstallation():
    for x in possibleLocations:
        try:
            if Path(x).is_file():
                return x
        except:
            pass
    return ""

def initPlatform():
    globals.platformHome = "~"
    globals.platform = globals.Platform.Linux
    globals.filename = searchForInstallation()
