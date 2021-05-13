import tkinter as tk
import globals

def initConfigValues():
    global configStorage
    configStorage = {}

class EntryWithPlaceholder(tk.Entry):
    def __init__(self, master=None, placeholder="PLACEHOLDER", color='grey'):
        super().__init__(master)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color

    def foc_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()

def apply(id, inputs, window):
    global configStorage
    for val,clas,name in inputs:
        try:
            v = str(clas(val.get()))
            configStorage[id + name] = v
        except Exception:
            pass
    window.destroy()

def makeConfig(addon):
    window = tk.Toplevel()
    window.resizable(False, False)
    window.winfo_toplevel().title("Configure Addon")

    frame = tk.Frame(window)
    frame.pack(fill="x")

    inputs = []
    for i, option in enumerate(addon.conf.split("|")):
        x = tk.Label(frame, text=option.split(":")[0], font=globals.FONT)
        x.grid(row=i, column=0, padx=5, pady=2.5)
        typ = option.split(":")[1]
        if typ == "int":
            y = EntryWithPlaceholder(frame, placeholder="INTEGER")
            y.grid(row=i, column=1, padx=5)
            inputs.append((y, int, option.split(":")[0]))

    button_close = tk.Button(window, text="Cancel", font=globals.FONT, command=window.destroy, fg="red", activebackground="#E05050")
    button_close.pack(side="right", padx=5, pady=5)
    button_apply = tk.Button(window, text="Apply", font=globals.FONT, command=lambda:apply(addon.id, inputs, window), fg="green", activebackground="#50E050")
    button_apply.pack(side="right", pady=5)
