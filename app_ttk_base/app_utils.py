import json

def load_json(filename:str, default:dict=None)->dict|None:
    """
    Read a json file and convert it in a dictionary.
    :param filename: the full name of the json file.
    :param default: the default dictionary, if any.
    :return: the dictionary.
    """
    try:
        with open(filename, "r", encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e :
        print(f"Error loading {filename}: {e}")
        print(f"Return default...")
        data = default
    return data

def save_json(data:dict, filename:str):
    """
    Save the data (a dictionary) in a json file.
    :param data: the data to save.
    :param filename: the name of the json file.
    :return:
    """
    try:
        with open(filename, "w", encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error saving data in {filename}: {e}")

