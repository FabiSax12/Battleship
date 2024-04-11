from enums import *

# Global variables

game_data = {
    "players": [],
    "board_1": [],
    "board_2": [],
    "button_width": 30,
    "board_rows": 10,
    "board_columns": 20,
}

board_1 = []
board_2 = []

ships = {
    Ship.DESTRUCTOR: ["b1.png"],
    Ship.CRUCERO: ["b21.png", "b22.png"],
    Ship.ACORAZADO: ["b31.png", "b32.png", "b33.png"]
}

ships_Tkinter_images = {
    Ship.DESTRUCTOR: {orientation: [] for orientation in Orientation},
    Ship.CRUCERO: {orientation: [] for orientation in Orientation},
    Ship.ACORAZADO: {orientation: [] for orientation in Orientation},
}