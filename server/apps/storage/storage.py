import os
import json
import re


STORAGE_PATH = os.path.join(os.getcwd(), "storage")
TOKEN_PATH = "__tokens.json"


def init():
    if not os.path.exists(STORAGE_PATH):
        os.mkdir(STORAGE_PATH)


app_id_re = re.compile("^[A-Za-z0-9_.-]+$")


def check_app_id(app_id: str):
    m = app_id_re.match(app_id)
    return bool(m) and app_id != TOKEN_PATH
