from pathlib import Path
import os, sys

def resource_path():
    """Devuelve la ruta correcta a un recurso, en dev o ejecutable."""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = Path(__file__).parent.parent
        Path(__file__).parent.parent
    return base_path

# GLOBAL 
BASE_DIR = resource_path()
SRC_PATH = BASE_DIR.joinpath("src")
USER_ICONS_PATH = BASE_DIR.joinpath("src").joinpath("user").joinpath("icons")
APP_ICONS_PATH = BASE_DIR.joinpath("src").joinpath("app").joinpath("icons")

NOTIFICATIONS = []