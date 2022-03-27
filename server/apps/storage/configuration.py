import os
import json
from .storage import STORAGE_PATH, TOKEN_PATH


def save_configuration(app_id: str, config: dict):
    with open(os.path.join(STORAGE_PATH, app_id), "w+") as f:
        json.dump(config, f, indent=4)


def get_configuration(app_id: str) -> str:
    p = os.path.join(STORAGE_PATH, app_id)
    if not os.path.exists(p):
        return "{}"
    with open(os.path.join(STORAGE_PATH, app_id), "r") as f:
        return f.read()


def get_configuration_json(app_id: str) -> str:
    return json.loads(get_configuration(app_id))


def get_all_configuration():
    files = os.listdir(STORAGE_PATH)
    files.remove(TOKEN_PATH)

    result = dict()
    for f in files:
        result[f] = get_configuration_json(app_id=f)
    return result
