import os
import json
from enums import *

# Global variables

game_data = {
    "players": [],
    "button_width": 30,
    "board_rows": 10,
    "board_columns": 20,
    "board_1": [],
    "board_2": [],
    "board_1_ships": [],
    "board_2_ships": []
}

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

def save_game_data(file_name: str = "game_data"):
    documents_path = os.path.join(os.getenv("HOME" if os.name == "posix" else "USERPROFILE"), "Documents")

    if not os.path.exists(f"{documents_path}/battleship_data"):
        os.makedirs(f"{documents_path}/battleship_data")

    game_data_path = os.path.join(documents_path, "battleship_data", f"{file_name}.json")

    game_data_copy = game_data.copy()
    game_data_copy.pop("board_1", None)
    game_data_copy.pop("board_2", None)

    with open(game_data_path, "w") as file:
        json.dump(game_data_copy, file)

def load_game_data(file_name: str = "game_data"):
    documents_path = os.path.join(os.getenv("HOME" if os.name == "posix" else "USERPROFILE"), "Documents")
    
    game_data_path = os.path.join(documents_path, "battleship_data", f"{file_name}.json")

    print(game_data_path)

    if os.path.exists(game_data_path):
        with open(game_data_path, "r") as file:
            new_game_data = json.load(file)

            for key, value in new_game_data.items():
                game_data[key] = value
        
    else:
        print(f"El archivo {file_name} no existe en la carpeta de datos del juego.")
        return None