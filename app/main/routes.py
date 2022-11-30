import os
from flask import render_template, send_file, redirect, url_for
from flask_login import current_user, login_required
from app.main import bp
from app import app


@bp.route("/")
@login_required
def main_page():
    if current_user.is_authenticated and current_user.role.name == 'admin':
        return redirect(url_for("dashboard.dashboard"))
    elif current_user.is_authenticated and current_user.role.name == 'user':
        return redirect(url_for("main.main_page"))
    else:
        return render_template('default/home.html', name="hello")


@bp.route('/uploads/<dir>/<filename>')
def download_file(dir, filename):
    return send_file(os.path.join(
        app.config["APP_PATH"],
        app.config["UPLOAD_PATH"],
        f'{dir}/{filename}'
    ))
