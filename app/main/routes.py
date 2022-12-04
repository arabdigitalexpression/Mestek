import os

from flask import render_template, send_file
from flask_login import login_required

from app import app
from app.main import bp


@bp.route("/")
@login_required
def main_page():
    return render_template('default/home.html', name="hello")


@bp.route('/uploads/<dir>/<filename>')
def download_file(dir, filename):
    return send_file(os.path.join(
        app.config["APP_PATH"],
        app.config["UPLOAD_PATH"],
        f'{dir}/{filename}'
    ))
