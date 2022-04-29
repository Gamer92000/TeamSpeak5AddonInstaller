from PIL import Image, ImageTk
import tkinter as tk
import webbrowser, globals, io, urllib.request, re
from threading import Thread
import requests

class Addon:
    def __init__(self, definitions):
        self.status = None
        self.installed = False
        self.name = definitions["name"]
        self.url = definitions["url"]
        self.description = definitions["description"]
        self.id = definitions["id"]
        self.info = definitions.get("info")
        self.objects = []
        try:
            imageData = urllib.request.urlopen(definitions['icon']).read()
            im = Image.open(io.BytesIO(imageData))
            im = im.resize((80, 80), Image.ANTIALIAS)
            self.image = ImageTk.PhotoImage(im)
        except Exception as e:
            print("Could not load image for addon: " + self.name)
            im = Image.new('RGBA', (80, 80), (100, 100, 100, 80))
            self.image = ImageTk.PhotoImage(im)

    def download(self):
        # download addon from self.url
        data = requests.get(self.url)
        if data.status_code != 200:
            raise Exception("Could not download addon")
        data = data.text
        # add id as comment to start and end of data
        data = '<!-- ' + self.id + ' -->\n' + data + '\n<!-- ' + self.id + ' -->'
        self.data = data

    def checkInstall(self):
        if (globals.filename == ""): return
        self.installed = self.id in open(globals.filename).read()

    def install(self):
        # lock UI
        globals.disableAllButtons()
        self.status.config(fg="#444", text="installing")

        # install addon
        try:
            if not hasattr(self, 'data'):
                self.download()
            globals.inplace_change(globals.filename, '</head>', self.data + '</head>')
        except Exception as e:
            print(e)

        # unlock UI
        globals.enableAllButtons()
        globals.showPage()

    def uninstall(self):
        # lock UI
        globals.disableAllButtons()
        self.status.config(fg="#444", text="uninstalling")

        # uninstall addon
        comment = '<!-- ' + self.id + ' -->'
        regex = re.compile(comment + '(.*)' + comment)
        globals.inplace_change(globals.filename, regex, '')

        # unlock UI
        globals.enableAllButtons()
        globals.showPage()

    def createFrame(self, app):
        container = tk.Frame(app.objectContainer)
        container.pack(side="top", fill=tk.X, padx=5, pady=5)
        self.objects.append(container)

        title = tk.Label(container, text=self.name, font=globals.FONT)
        title.grid(row=0, column=0, sticky="w", columnspan=3)
        self.objects.append(title)

        if self.info:
            f = globals.FONT.copy()
            f.config(underline = True, size=9)
            more = tk.Label(container, text="more", cursor="hand2", fg="blue", font=f)
            more.bind("<Button-1>", lambda e: webbrowser.open_new(self.info))
            more.grid(row=0, column=0, sticky="e", columnspan=3)
            self.objects.append(more)

        self.status = tk.Label(container, text="installed" if self.installed else "not installed", fg="green" if self.installed else "#000", font=globals.FONT)
        self.status.grid(row=1, column=0, pady=5)
        self.objects.append(self.status)

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
