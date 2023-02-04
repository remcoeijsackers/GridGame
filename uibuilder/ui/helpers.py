import tkinter as tk

def destroyChilds(parent: tk.Frame):
    for child in parent.winfo_children():
        child.destroy()