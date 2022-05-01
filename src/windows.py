import globals, string
from ctypes import windll
from pathlib import Path

def is_admin():
    try:
        return windll.shell32.IsUserAnAdmin()
    except Exception:
        return False

# iterates through drive letters in alphabetical order and takes the first match as path
def searchForInstallation():
    ts_dir = "/Program Files/TeamSpeak/html/client_ui/index.html"
    # try default drive
    if Path('C:' + ts_dir).exists():
        return Path('C:' + ts_dir)
    else:
    # if not found in C drive
        possibleLocations = get_drives()
        for drive in possibleLocations:
            if Path(drive).exists():
                return Path(drive + ts_dir)
    # ...my friend, you do not have teamspeak 5 installed!

def get_drives():
    drives = []
    bitmask = windll.kernel32.GetLogicalDrives()
    for letter in string.ascii_uppercase:
        if bitmask & 1 and letter != 'C':
            drives.append(letter + ':')
        bitmask >>= 1
    # return a list of connected drives, except C drive
    return drives


def initPlatform():
    globals.platformHome = "%userprofile%"
    globals.platform = globals.Platform.Windows
    globals.filename = searchForInstallation()