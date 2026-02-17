import json
import os


def load_json(path: str) -> list: # type: ignore
    
    if not os.path.exists(path):
        return [] # type: ignore

    try:
        with open(path, "r") as file:
            data = json.load(file)
            return data
    except:
        # File exists but is empty or corrupted
        return [] # type: ignore


def save_json(path: str, data): # type: ignore
    with open(path, "w") as file:
        json.dump(data, file, indent=4)


def remove_from_json(target_id: str, path: str) -> bool:
    if not os.path.exists(path):
        return False

    try:
        with open(path, "r") as file:
            data = json.load(file)

        if not isinstance(data, list):
            raise ValueError("JSON structure must be a list of objects")

        original_length = len(data) # type: ignore

        data = [item for item in data if item.get("id") != target_id] # type: ignore

        if len(data) == original_length: # type: ignore
            return False  

        with open(path, "w") as file:
            json.dump(data, file, indent=4)

        return True

    except json.JSONDecodeError:
        return False


def add_to_json(new_entry: dict, path: str) -> None: # type: ignore

    if os.path.exists(path):
        try:
            with open(path, "r") as file:
                data = json.load(file)
        except json.JSONDecodeError:
            data = []
    else:
        data = []

    if not isinstance(data, list):
        raise ValueError("JSON structure must be a list of objects")

    data.append(new_entry) # type: ignore

    with open(path, "w") as file:
        json.dump(data, file, indent=4)
