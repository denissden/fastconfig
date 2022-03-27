import json

from flask import Blueprint, request
import logging
from ..storage import save_token, \
    check_token, \
    get_configuration, \
    save_configuration, \
    check_master_token, \
    get_all_configuration, \
    check_app_id
import uuid

configuration = Blueprint("configuration", __name__)


def app_token_valid(app_id: str):
    token = request.headers.get("token")

    if not check_token(app_id, token.strip()):
        logging.warning(f"{app_id=} invalid {token=}")
        return False

    logging.info(f"{app_id=} token {token[:5]}.. valid")
    return True


def master_token_valid():
    token = request.headers.get("token")

    if not check_master_token(token.strip()):
        logging.warning(f"Invalid master {token=}")
        return False

    logging.info(f"Master token {token[:5]}.. valid")
    return True


@configuration.route("/configuration/<app_id>", methods=["GET", "PUT"])
def config_handler(app_id: str):
    if not app_token_valid(app_id) and not master_token_valid():
        return "Invalid token", 401
    if not check_app_id(app_id):
        return "Invalid app_id", 400

    logging.info(f"Configuration {app_id=}")

    if request.method == "GET":
        return get_configuration(app_id)

    elif request.method == "PUT":
        conf = request.get_json(force=True)
        save_configuration(app_id, conf)
        return "ok"

    return "Idk", 400


@configuration.route("/configuration", methods=["GET"])
def all_config_handler():
    if not master_token_valid():
        return "Invalid token", 401

    logging.info(f"All configuration")

    all_configuration = get_all_configuration()
    return json.dumps(all_configuration)


@configuration.route("/token/<app_id>/new", methods=["GET"])
def token_handler(app_id: str):
    if not master_token_valid():
        return "Invalid token", 401
    if not check_app_id(app_id):
        return "Invalid app_id", 400

    logging.info(f"New token request {app_id=}")

    new_token = str(uuid.uuid4())
    save_token(app_id, new_token)

    return new_token
