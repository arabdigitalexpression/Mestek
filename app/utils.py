from os import path, remove, makedirs
from uuid import uuid4

from flask import abort, url_for, send_from_directory, current_app

from app import app

from werkzeug.utils import secure_filename


def save_file(directory, file):
    # Generate a unique identifier and append it to the filename to avoid collisions
    unique_filename = f"{uuid4().hex}_{secure_filename(file.filename)}"

    # Construct the full path for the file to be saved
    full_directory_path = path.join(current_app.config["APP_PATH"], current_app.config["UPLOAD_PATH"], directory)

    # Ensure the directory exists
    if not path.exists(full_directory_path):
        makedirs(full_directory_path)

    # Attempt to save the file
    try:
        file.save(path.join(full_directory_path, unique_filename))
    except Exception as e:
        current_app.logger.error(f"Failed to save file: {str(e)}")
        abort(500)

    # Return the URL for the saved file
    return url_for("main.download_file", directory=directory, filename=unique_filename, _external=True)


def get_file_response(directory, filename):
    full_path = path.join(
        current_app.config["APP_PATH"],
        current_app.config["UPLOAD_PATH"],
        directory
    )
    return send_from_directory(full_path, filename)


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
