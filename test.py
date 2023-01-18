import tkinter as tk

class App(object):

    def __init__(self, parent):

        self.root = parent
        self.root.title("Main Frame")
        self.frame = tk.Frame(parent)
        self.frame.pack()
        label = tk.Label(self.frame, text = "This is the main frame")
        label.grid()
        btn = tk.Button(self.frame, text= "Open the popup window", command = lambda : self.pop_up())
        btn.grid(row=1)

    def pop_up(self):
        self.root.withdraw()
        popUp(self)

class popUp(tk.Toplevel):

    def __init__(self, original):

        self.original_frame = original
        tk.Toplevel.__init__(self)
        self.transient(root)
        self.geometry("260x210")
        self.lift()
        label = tk.Label(self, text = "This is Popup window")
        label.grid()
        btn = tk.Button(self, text ="Close", command= lambda : self.on_close())
        btn.grid(row =1)

    def on_close(self):
        self.destroy()
        root.update()
        root.deiconify()

if __name__ == "__main__":

    root = tk.Tk()
    app = App(root)
    root.geometry("200x150")
    root.mainloop()