from flask import render_template
from flask_login import login_required

from app.main import bp
from app.utils import get_file_response


@bp.route("/")
@login_required
def main_page():
    return render_template('default/home.html', name="hello")


@bp.route('/uploads/<directory>/<filename>')
def download_file(directory, filename):
    return get_file_response(directory, filename)
