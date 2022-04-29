import sys
import tkinter as tk
from tkinter import ttk, font
from tkinter.filedialog import askopenfilename
from addon import Addon
import yaml, io, math, webbrowser, globals, re
import requests

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.winfo_toplevel().title("Unofficial TeamSpeak 5 Addon Installer")
        # outer Frame
        self.outerFrame = tk.Frame(self)
        self.outerFrame.pack(side="top", fill=tk.X)

        # index Frame
        self.indexSelectFrame = tk.Frame(self.outerFrame)
        self.indexSelectFrame.pack(side="top", fill=tk.X, padx = 5, pady=5)

        # index Frame -> select Button
        self.selectButton = tk.Button(self.indexSelectFrame, text="Select Index File", command=self.selectFile, font=globals.FONT)
        self.selectButton.grid(row=0, column=0)

        # index Frame -> Label
        self.indexLabel = tk.Label(self.indexSelectFrame, text=globals.filename if globals.filename else "not yet selected", font=globals.FONT)
        self.indexLabel.grid(row=0, column=1, padx = 5)

        # object container wrapper
        self.objectContainer = tk.Frame(self.outerFrame)
        self.objectContainer.pack(side="top", fill=tk.X)

        self.containerList = []

        # control area bottom
        self.spacer0 = ttk.Separator(self.outerFrame)
        self.spacer0.pack(side="top", fill=tk.X)

        self.interact = tk.Frame(self.outerFrame)
        self.interact.pack(side="top", fill=tk.X, padx=5, pady=5)

        # page selection < page / pages >
        self.prev = tk.Button(self.interact, text="<", command=self.prev, state=tk.DISABLED, font=globals.FONT)
        self.prev.grid(row=0, column=0, padx=5)

        self.page = tk.Label(self.interact, text="1 / " + str(MAXPAGES), font=globals.FONT)
        self.page.grid(row=0, column=1, padx=5)

        self.next = tk.Button(self.interact, text=">", command=self.next, state=tk.DISABLED if MAXPAGES<=1 else tk.NORMAL, font=globals.FONT)
        self.next.grid(row=0, column=2, padx=5)

        # support me :)
        f = globals.FONT.copy()
        f.config(underline = True, size=9)
        self.support = tk.Label(self.interact, text="support me", fg="blue", cursor="hand2", font=f)
        self.support.bind("<Button-1>", lambda _: webbrowser.open_new("https://www.buymeacoffee.com/JulianImhof"))
        self.support.grid(row=0, column=0, columnspan=4)

        # QUIT button
        self.quit = tk.Button(self.interact, text="QUIT", fg="red", activebackground="#E05050", command=self.master.destroy, font=globals.FONT)
        self.quit.grid(row=0, column=3, sticky="e")
        self.interact.grid_columnconfigure(3, weight=1)

    def selectFile(self):
        globals.filename = askopenfilename(title='Find index.html in client_ui!', filetypes=[(globals.filetypeString, globals.filetype)], initialdir=globals.platformHome)
        if not globals.filename or not globals.filename.endswith("index.html"): return
        self.indexLabel["text"] = globals.filename
        self.indexLabel.config(fg="#000")
        globals.disableAllButtons()
        globals.enableAllButtons()
        showPage(currpage)

    def prev(self):
        global currpage
        currpage = max(currpage - 1, 0)
        self.page["text"] = str(currpage + 1) + " / " + str(MAXPAGES)
        showPage(currpage)
        if currpage == 0: self.prev.config(state=tk.DISABLED)
        if currpage != MAXPAGES-1: self.next.config(state=tk.NORMAL)

    def next(self):
        global currpage
        currpage = min(currpage + 1, MAXPAGES-1)
        self.page["text"] = str(currpage + 1) + " / " + str(MAXPAGES)
        showPage(currpage)
        if currpage != 0: self.prev.config(state=tk.NORMAL)
        if currpage == MAXPAGES-1: self.next.config(state=tk.DISABLED)

spacers = []
def showPage(i):
    global spacers
    for addon in addons:
        addon.checkInstall()

    firstIndex = ITEMSPERPAGE * i
    lastIndex = firstIndex + ITEMSPERPAGE
    # clear page
    for addon in addons:
        addon.destroyFrame()
    for spacer in spacers:
        spacer.pack_forget()
        spacer.destroy()
    spacers = []
    
    # show page
    for addon in addons[firstIndex:lastIndex]:
        spacer = ttk.Separator(app.objectContainer)
        spacer.pack(side="top", fill=tk.X)
        spacers.append(spacer)
        addon.createFrame(app)

root = tk.Tk()
root.resizable(False, False)

# config
ITEMSPERPAGE = 3

# internal
currpage = 0
prevButtonState = None
nextButtonState = None

globals.init()

conf = None
try:
    conf = yaml.safe_load(open("TS5AddonInstaller.yml", "r"))
except:
    pass

# fetch possible addons
try:                # try custom lookup server from config file
    if conf == None: raise Exception()
    configData = requests.get(str(conf['url'])).text
except:             # fallback to default lookup server
    configRequest = requests.get("https://raw.githubusercontent.com/Gamer92000/TeamSpeak5AddonInstaller/master/server/addons.yml")
    if configRequest.status_code != 200:
        print("Error: Could not fetch addon list!")
        sys.exit(1)
    configData = configRequest.text

config = yaml.safe_load(io.StringIO(configData))

if config.get('addons') is None:
    print("No addons found!")

n = len(config["addons"])

MAXPAGES = math.ceil(n / ITEMSPERPAGE)

addons = []
for addon in config['addons']:
    addons.append(Addon(addon))

app = Application(master=root)
globals.app = app
globals.showPage = lambda: showPage(currpage)

showPage(0)

app.mainloop()
