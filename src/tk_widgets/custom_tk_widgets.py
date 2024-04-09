import tkinter as tk
from enums import Color

def Button(window: tk.Tk, text: str = "", on_click = None) -> tk.Button:
    return tk.Button(
        window, 
        text = text, 
        font = ("Times New Roman", 17), 
        bg = Color.BLACK.value, 
        fg = Color.WHITE.value,
        command=on_click
    )
    
def Label(window: tk.Tk, text: str = "", font_size = 15) -> tk.Label:
    return tk.Label(
        window,
        text = text,
        font=("Times New Roman", font_size),
    )

def Entry(window: tk.Tk, font_size = 15 ) -> tk.Entry:
    return tk.Entry(
        window,
        font=("Times New Roman", font_size)
    )