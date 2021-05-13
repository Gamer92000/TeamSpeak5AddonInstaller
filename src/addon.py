from PIL import Image, ImageTk
import tkinter as tk
import globals, io, urllib.request, re
import config
from threading import Thread

class Addon:
    def __init__(self, name, definitions):
        self.name = name
        self.status = None
        self.installed = False
        self.typ = definitions.get("type")
        self.url = definitions.get("url")
        self.conf = definitions.get("config")
        self.description = definitions.get("description")
        self.id = definitions.get("identifier")
        self.objects = []
        self.config = definitions
        if self.conf:
            for n,t,d in map(lambda x: x.split(":"), self.conf.split("|")):
                config.configStorage[self.id + n] = d
        try:
            imageData = urllib.request.urlopen(definitions['image']).read()
            im = Image.open(io.BytesIO(imageData))
            im = im.resize((80, 80), Image.ANTIALIAS)
            self.image = ImageTk.PhotoImage(im)
            self.im = im
        except Exception as e:
            print(e)
            im = Image.new('RGBA', (80, 80), (255, 0, 0, 0))
            self.image = ImageTk.PhotoImage(im)

    def checkInstall(self):
        self.installed = self.id in open(globals.filename).read()

    def install(self):
        globals.disableAllButtons()
        self.status.config(fg="#444", text="installing")

        confStr = self.config['install']
        for conf in re.findall(r"{{([^\}]*)}}", confStr):
            s = config.configStorage.get(self.id + conf)
            s = s if s else ""
            confStr = re.sub("{{" + conf + "}}", s, confStr)

        globals.inplace_change(globals.filename, '</head>', confStr + '</head>')
        globals.enableAllButtons()
        globals.showPage()

    def uninstall(self):
        globals.disableAllButtons()
        self.status.config(fg="#444", text="uninstalling")

        confStr = self.config['install']
        for i in "\\?+*[]().^$":
            confStr = confStr.replace(i, "\\" + i)
        for conf in re.findall("{{([^\}]*)}}", confStr):
            confStr = re.sub("{{" + conf+ "}}", '[^\?\=\&]*', confStr)
        for i in "{}":
            confStr = confStr.replace(i, "\\" + i)

        globals.inplace_change(globals.filename, confStr, '')
        globals.enableAllButtons()
        globals.showPage()

    def createFrame(self, app):
        container = tk.Frame(app.objectContainer)
        container.pack(side="top", fill=tk.X, padx=5, pady=5)
        self.objects.append(container)

        title = tk.Label(container, text=self.name + " - " + self.typ, font=globals.FONT)
        title.grid(row=0, column=0, sticky="w", columnspan=3)
        self.objects.append(title)

        if self.url:
            f = globals.FONT.copy()
            f.config(underline = True, size=9)
            more = tk.Label(container, text="more", cursor="hand2", fg="blue", font=f)
            more.bind("<Button-1>", lambda e: webbrowser.open_new(url))
            more.grid(row=0, column=0, sticky="e", columnspan=3)
            self.objects.append(more)

        self.status = tk.Label(container, text="installed" if self.installed else "not installed", fg="green" if self.installed else "#000", font=globals.FONT)
        self.status.grid(row=1, column=0, pady=5)
        self.objects.append(self.status)

        if self.conf:
            conf = tk.Button(container, text="Configure", font=globals.FONT, command=lambda: config.makeConfig(self), state=tk.DISABLED if self.installed else tk.NORMAL)
            conf.grid(row=2, column=0, pady=5)
            self.objects.append(conf)

        button = tk.Button(container, text="UNINSTALL" if self.installed else "INSTALL", relief="sunken" if self.installed else "raised", state=tk.DISABLED if globals.filename=="" else tk.NORMAL, command=self.toggleInstall, font=globals.FONT)
        button.grid(row=3, column=0, pady=5)
        self.objects.append(button)

        image = tk.Label(container, image=self.image)
        image.grid(row=1, column=1, padx=5, rowspan=3)
        self.objects.append(image)
        container.grid_columnconfigure(1, weight=1)

        description = tk.Message(container, text=self.description, width=250, font=globals.FONT)
        description.grid(row=1, column=2, rowspan=3)
        self.objects.append(description)

    def destroyFrame(self):
        for elem in self.objects[::-1]:
            if elem.winfo_manager() == "grid":
                elem.grid_forget()
            else:
                elem.pack_forget()
            elem.destroy()
        self.objects = []

    def toggleInstall(self):
        if self.installed:
            Thread(target=self.uninstall, daemon=True).start()
        else:
            Thread(target=self.install, daemon=True).start()