from enum import Enum
import sys, linux, windows, mac, ctypes, re
from tkinter import font
import tkinter as tk

class Platform(Enum):
    Windows = 0
    Linux = 1
    Mac = 2
    Non = 3

def init():
    global platform, platformHome, filename, filetype, filetypeString, FONT
    platform = Platform.Non
    platformHome = ""
    filename = ""
    filetype = "index.html"
    filetypeString = "Main TeamSpeak File"
    FONT = font.Font(family="Ubuntu Thin", size=10)

    if sys.platform.startswith('win32'):
        windows.initPlatform()
    elif sys.platform.startswith('linux'):
        linux.initPlatform()
    elif sys.platform.startswith('darwin'):
        mac.initPlatform()
    else:
        print(f"No OS?! ({sys.platform})")

def fixWindowsUAC():
    if platform == Platform.Windows and not windows.is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        app.master.destroy()

def disableAllButtons():
    global prevButtonState, nextButtonState
    app.selectButton.config(state=tk.DISABLED)
    prevButtonState = app.prev['state'] == tk.NORMAL
    nextButtonState = app.next['state'] == tk.NORMAL
    app.prev.config(state=tk.DISABLED)
    app.next.config(state=tk.DISABLED)
    app.quit.config(state=tk.DISABLED)

def enableAllButtons():
    app.selectButton.config(state=tk.NORMAL)
    if prevButtonState: app.prev.config(state=tk.NORMAL)
    if nextButtonState: app.next.config(state=tk.NORMAL)
    app.quit.config(state=tk.NORMAL)


def inplace_replace(filename, old_regex, new_regex):
    with open(filename) as f:
        s = f.read()
    try:
        with open(filename, 'w') as f:
            s = re.sub(old_regex, new_regex, s)
            f.write(s)
    except Exception as e:
        print(e)
        # this damn windows uac....
        fixWindowsUAC()

def inplace_remove(filename, splitter):
    with open(filename) as f:
        s = f.read()
    try:
        with open(filename, 'w') as f:
            # remove everything between the first and second occurence of the splitter
            s = s.split(splitter)[0] + s.split(splitter)[2]
            f.write(s)
    except Exception as e:
        print(e)
        # this damn windows uac....
        fixWindowsUAC()