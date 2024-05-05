
import json


def load_configuration():
    # Cargar la configuración desde el archivo config.json si existe
    try:
        with open("config.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        # Si el archivo no existe, retornar un diccionario vacío
        return {}
