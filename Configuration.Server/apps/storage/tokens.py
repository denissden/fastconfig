import os
import json
from .storage import STORAGE_PATH, TOKEN_PATH

MASTER_TOKEN_ID = "__MASTER"


def get_tokens() -> dict:
    p = os.path.join(STORAGE_PATH, TOKEN_PATH)
    if not os.path.exists(p):
        return dict()
    with open(p, "r") as f:
        return json.load(f)


def save_tokens(tokens: dict):
    with open(os.path.join(STORAGE_PATH, TOKEN_PATH), "w+") as f:
        json.dump(tokens, f, indent=4)


def get_token(app_id: str):
    token_conf = get_tokens()

    if app_id in token_conf:
        return token_conf[app_id]
    else:
        return None


def save_token(app_id: str, token: str):
    token_conf = get_tokens()
    token_conf[app_id] = token
    save_tokens(token_conf)


def check_token(app_id: str, token_to_check: str):
    token = get_token(app_id)
    if token is not None and token == token_to_check:
        return True
    else:
        return False


def get_master_token():
    return get_token(MASTER_TOKEN_ID)


def set_master_token(token: str):
    return save_token(MASTER_TOKEN_ID, token)


def check_master_token(token_to_check: str):
    return check_token(MASTER_TOKEN_ID, token_to_check)
