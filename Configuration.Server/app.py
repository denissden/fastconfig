import logging
import uuid

from flask import Flask
import os


def create_app():
    app = Flask(__name__)

    from apps.configuration import configuration
    app.register_blueprint(configuration)
    logging.root.setLevel(logging.INFO)

    from apps.storage import init as storage_init, get_master_token, set_master_token, STORAGE_PATH
    storage_init()
    logging.info(f"Configuration storage at {STORAGE_PATH}")
    if (master_token := get_master_token()) is not None:
        logging.info(f"Found master token {master_token[:5]}..")
    else:
        new_token = str(uuid.uuid4())
        set_master_token(new_token)
        logging.info(f"Generated new master token {new_token}")

    return app