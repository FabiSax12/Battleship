import tkinter as tk
from enums import Color

class Frame(tk.Frame):
    def __init__(self, window: tk.Tk, *args, **kargs):
        super().__init__(
            window,
            *args, **kargs
        )

class Button(tk.Button):
    def __init__(self, window: tk.Tk, text: str = "", on_click = None, *args, **kargs):
        super().__init__(
            window, 
            text = text, 
            font = ("Times New Roman", 17), 
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
            font=("Times New Roman", font_size),
            *args, **kargs
        )

class Entry(tk.Entry):
    def __init__(self, window: tk.Tk, font_size = 15, *args, **kargs):
        super().__init__(
            window,
            font=("Times New Roman", font_size),
            *args, **kargs
        )