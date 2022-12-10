from flask import render_template
from flask_login import login_required

from app.main import bp
from app.models import Space, Category, Tool
from app.utils import get_file_response


@bp.route("/")
@login_required
def main_page():
    return render_template('default/home.html', name="hello")


@bp.route('/uploads/<directory>/<filename>')
def download_file(directory, filename):
    return get_file_response(directory, filename)


@bp.route('/spaces/')
def spaces_list():
    spaces = Space.query.all()
    return render_template("default/space/index.html", spaces=spaces)


@bp.route('/spaces/<int:id>/')
def space_details(id):
    space = Space.query.get(id)
    categories = Category.query.all()
    return render_template("default/space/details.html", space=space, categories=categories)


@bp.route('/tools/')
def tools_list():
    tools = Tool.query.all()
    return render_template("default/tool/index.html", tools=tools)


@bp.route('/tools/<int:id>/')
def tool_details(id):
    tool = Tool.query.get(id)
    categories = Category.query.all()
    return render_template("default/tool/details.html", tool=tool, categories=categories)
