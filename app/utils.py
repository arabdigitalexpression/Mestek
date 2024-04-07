from os import path, remove, makedirs
from uuid import uuid4
from PIL import Image

from flask import url_for, send_from_directory, current_app

from app import app


def process_and_save_image(directory, file, max_dimension=1080):
    # Construct the full path for the file to be saved
    full_directory_path = path.join(current_app.config["UPLOAD_PATH"], directory)

    # Ensure the directory exists
    if not path.exists(full_directory_path):
        makedirs(full_directory_path)

    # Convert the uploaded file to a PIL Image object
    image = Image.open(file.stream)

    # Resize the image if either dimension is greater than max_dimension
    if image.width > max_dimension or image.height > max_dimension:
        image.thumbnail((max_dimension, max_dimension), Image.Resampling.LANCZOS)

    # Generate a unique identifier and append it to the filename to avoid collisions saved as WebP
    webp_filename = f"{uuid4().hex}.webp"
    webp_path = path.join(full_directory_path, webp_filename)
    image.save(webp_path, 'WEBP', quality=90)

    # Return the URL for the saved WebP file
    return url_for("main.download_file", directory=directory, filename=webp_filename, _external=True)


def get_file_response(directory, filename):
    full_path = path.join(current_app.config["UPLOAD_PATH"], directory)
    return send_from_directory(full_path, filename)


def remove_file(directory, filename):
    try:
        remove(path.join(app.config["UPLOAD_PATH"], f'{directory}/{filename}'))
        return True
    except OSError as error:
        return error.strerror
