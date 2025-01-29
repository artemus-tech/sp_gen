import json
import os.path


def load_settings(file_name='app.settings.json'):
    path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(path, file_name)
    try:
        with open(file_path, 'r') as f:
            settings = json.load(f)
        return settings
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return None


