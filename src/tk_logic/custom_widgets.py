import tkinter as tk
from enums import Color

def center_widget(self: tk.Widget, window: tk.Tk, axis: str, x = None, y = None):
    if axis == "x":
        self.place(x=(window.winfo_reqwidth() // 2 - self.winfo_reqwidth()) // 2, y=y)
    else:
        self.place(y=(window.winfo_reqheight() - self.winfo_reqheight()) // 2, x=x)

class Button(tk.Button):
    def __init__(self, window: tk.Tk, text: str = "", on_click = None, *args, **kargs):
        super().__init__(
            window, 
            text = text, 
            font = ("Terminal", 17), 
            bg = Color.BLACK.value, 
            fg = Color.WHITE.value,
            command=on_click,
            *args, **kargs
       )

class Label(tk.Label):
    def __init__(self, window: tk.Tk, text: str = "", font_size = 15, *args, **kargs):
        super().__init__(
            window,
            text = text,
            font=("Terminal", font_size),
            *args, **kargs
        )

class Entry(tk.Entry):
    def __init__(self, window: tk.Tk, font_size = 15, *args, **kargs):
        super().__init__(
            window,
            font=("Terminal", font_size),
            *args, **kargs
        )

class Div(tk.Frame):
    def __init__(self, window: tk.Tk, *args, **kargs):
        super().__init__(window,*args, **kargs)
        # self.pack_propagate(False)

    def title(self, title: str):
        title_label = Label(self, title, 20)
        title_label.pack(side=tk.TOP, fill=tk.X, expand=True)

    def center(self, window: tk.Tk, axis: str, x = None, y = None):
        center_widget(self, window, axis, x, y)

class Scrollbar(tk.Scrollbar):
    def __init__(self, window: tk.Tk, *args, **kargs):
        super().__init__(window, *args, **kargs)
    
    def axis(self, axis: str):
        if axis == "x":
            self.pack(side=tk.BOTTOM, fill=tk.X)
        else:
            self.pack(side=tk.RIGHT, fill=tk.Y)

class Listbox(tk.Listbox):
    def __init__(self, window: tk.Tk, *args, **kargs):
        super().__init__(window, *args, **kargs)
        self.config(font=("Terminal", 15), relief=tk.FLAT, )
    
    def _action_and_destroy(self, action):
        selection = self.get(self.curselection()[0])
        self.winfo_toplevel().destroy()
        action(selection)

    def double_click(self, action, destroy = False):
        self.bind(
            "<Double-Button-1>", 
            lambda event: self._action_and_destroy(action) if destroy 
                    else action(self.get(self.curselection()[0]))
        )