import tkinter as tk

def destroyChilds(parent: tk.Frame):
    # This hack is probably no longer needed.
    try:
        for child in parent.winfo_children():
            child.destroy()
    except tk.TclError:
        pass