
import json
from pathlib import Path

def relative_to_assets(path: str) -> Path:
    script_path = Path(__file__).resolve().parent
    # Asumiendo que la carpeta 'assets' está en el mismo nivel que el script
    assets_path = script_path 
    return assets_path / Path(path)

def load_configuration():
    # Cargar la configuración desde el archivo config.json si existe
    try:
        config_path = relative_to_assets("config.json")
        with open(config_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        # Si el archivo no existe, retornar un diccionario vacío
        return {}
