import globals
from pathlib import Path

possibleLocations = ["A:\Program Files\TeamSpeak\html\client_ui\index.html",\
                     "B:\Program Files\TeamSpeak\html\client_ui\index.html",\
                     "C:\Program Files\TeamSpeak\html\client_ui\index.html",\
                     "D:\Program Files\TeamSpeak\html\client_ui\index.html",\
                     "E:\Program Files\TeamSpeak\html\client_ui\index.html",\
                     "F:\Program Files\TeamSpeak\html\client_ui\index.html",\
                     "G:\Program Files\TeamSpeak\html\client_ui\index.html",\
                     "H:\Program Files\TeamSpeak\html\client_ui\index.html",\
                     "I:\Program Files\TeamSpeak\html\client_ui\index.html",\
                     "J:\Program Files\TeamSpeak\html\client_ui\index.html"]

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False

def searchForInstallation():
    for x in possibleLocations:
        try:
            if Path(x).is_file():
                return x
        except: pass
    return ""

def initPlatform():
    globals.platformHome = "%userprofile%"
    globals.platform = globals.Platform.Windows
    globals.filename = searchForInstallation()
