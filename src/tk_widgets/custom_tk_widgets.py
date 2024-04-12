import tkinter as tk
from enums import Color

def Div(window: tk.Tk, *args, **kargs) -> tk.Frame:
    return tk.Frame(
        window,
        *args, **kargs
    )

# class miBoton(tk.Button):
#     def __init__(self, window: tk.Tk, text: str = "", on_click = None, *args, **kargs):
#         super().__init__(
#             window, 
#             text = text, 
#             font = ("Times New Roman", 17), 
#             bg = Color.BLACK.value, 
#             fg = Color.WHITE.value,
#             command=on_click,
#             *args, **kargs
#        )
def Button(window: tk.Tk, text: str = "", on_click = None,  *args, **kargs) -> tk.Button:
    return tk.Button(
        window, 
        text = text, 
        font = ("Times New Roman", 17), 
        bg = Color.BLACK.value, 
        fg = Color.WHITE.value,
        command=on_click,
         *args, **kargs
    )
    
def Label(window: tk.Tk, text: str = "", font_size = 15, *args, **kargs) -> tk.Label:
    return tk.Label(
        window,
        text = text,
        font=("Times New Roman", font_size),
        *args, **kargs
    )

def Entry(window: tk.Tk, font_size = 15,  *args, **kargs ) -> tk.Entry:
    return tk.Entry(
        window,
        font=("Times New Roman", font_size),
        *args, **kargs
    )