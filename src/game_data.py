import os
import json
from enums import *

game_data = {
    "players": [],
    "button_width": 30,
    "board_rows": 10,
    "board_columns": 20,
    "board_1": [],
    "board_2": [],
    "board_1_ships": [],
    "board_2_ships": [],
    "saved_games": [],
    "turn": 1,
    "game_stage": GameStage.PLACING_SHIPS,
}

documents_path = os.path.join(os.getenv("HOME" if os.name == "posix" else "USERPROFILE"), "Documents")

def find_saved_games() -> None:
    """
    Find saved game files in the battleship_data directory and update the saved games list in game_data.
    If the battleship_data directory does not exist, create it.
    """
    try:
        directory = os.path.join(
            os.getenv("HOME" if os.name == "posix" else "USERPROFILE"), 
            "Documents", 
            "battleship_data"
        )
        game_data["saved_games"] = [file.split(".")[0] for file in os.listdir(directory) if file.endswith(".json")]
    except FileNotFoundError:
        os.makedirs(directory)

def save_game_data(file_name: str = "game_data") -> None:
    """
    Save the game data to a JSON file.

    Args:
        file_name: The name of the file to save the game data. Defaults to "game_data".
    """
    directory = os.path.join(
        os.getenv("HOME" if os.name == "posix" else "USERPROFILE"), 
        "Documents", 
        "battleship_data"
    )
    if not os.path.exists(directory):
        os.makedirs(directory)

    game_data_path = os.path.join(directory, f"{file_name}.json")

    game_data_copy = game_data.copy()
    game_data_copy.pop("board_1", None)
    game_data_copy.pop("board_2", None)
    game_data_copy.pop("saved_games", None)
    game_data_copy["game_stage"] = game_data_copy["game_stage"].name

    with open(game_data_path, "w") as file:
        json.dump(game_data_copy, file)

def load_game_data(file_name: str = "game_data") -> None:
    """
    Load game data from a JSON file.

    Args:
        file_name: The name of the file containing the game data. Defaults to "game_data".
    """
    game_data_path = os.path.join(documents_path, "battleship_data", f"{file_name}.json")

    if os.path.exists(game_data_path):
        with open(game_data_path, "r") as file:
            new_game_data = json.load(file)

            for key, value in new_game_data.items():
                game_data[key] = value

            game_data["game_stage"] = GameStage[new_game_data["game_stage"]]
    else:
        print(f"The file {file_name} does not exist in the game data folder.")
