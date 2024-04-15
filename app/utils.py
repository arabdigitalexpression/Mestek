from os import path, remove, makedirs
from itsdangerous import URLSafeTimedSerializer
from uuid import uuid4
from PIL import Image

from flask import url_for, send_from_directory, current_app, render_template

from app import app, mailjet


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


def generate_token(email):
    serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])
    return serializer.dumps(email, salt=app.config["SECURITY_PASSWORD_SALT"])


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])
    try:
        email = serializer.loads(
            token, salt=app.config["SECURITY_PASSWORD_SALT"], max_age=expiration
        )
        return email
    except Exception:
        return False


def send_email(to_email, to_name, template_name, template_data):
    email_html = render_template(template_name, **template_data)
    data = {
      'Messages': [
        {
          "From": {
            "Email": app.config['EMAIL_SENDER'],
            "Name": app.config['EMAIL_SENDER_NAME']
          },
          "To": [
            {
              "Email": to_email,
              "Name": to_name
            }
          ],
          "Subject": template_data.get('subject', 'Welcome!'),
          "HTMLPart": email_html
        }
      ]
    }
    result = mailjet.send.create(data=data)
    return result.status_code, result.json()


def send_confirmation(email, name):
    template_name = "emails/welcome_email.html"
    token = generate_token(email)
    confirm_url = url_for('auth.confirm_email', token=token, _external=True)
    template_data = {
        'name': name,
        'confirm_url': confirm_url,
        'subject': 'تأكيد بريدك الإلكتروني'
    }
    return send_email(email, name, template_name, template_data)
