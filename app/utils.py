from os import path, remove
from uuid import uuid1

from flask import send_file, url_for

from app import app


def save_file(directory, file):
    filename = str(uuid1()) + file.filename.split()[-1]
    file.save(path.join(
        app.config["APP_PATH"],
        app.config["UPLOAD_PATH"],
        directory, filename
    ))
    return url_for(
        "main.download_file", directory=directory, filename=filename
    )


def get_file_response(directory, filename):
    return send_file(path.join(
        app.config["APP_PATH"],
        app.config["UPLOAD_PATH"],
        directory, filename
    ))


def remove_file(directory, filename):
    try:
        remove(path.join(
            app.config["APP_PATH"],
            app.config["UPLOAD_PATH"],
            f'{directory}/{filename}'
        ))
        return True
    except OSError as error:
        return error.strerror
