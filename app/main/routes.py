from flask import render_template
from flask_login import login_required

from app.enums import SpaceType
from app.main import bp
from app.models import Space, Category, Tool
from app.utils import get_file_response


@bp.route("/")
def main_page():
    spaces = Space.query.filter(Space.type != SpaceType.undefined).all()
    tools = Tool.query.all()
    types = [spaceType for spaceType in SpaceType if spaceType.value != 0]
    return render_template(
        'default/home.html', types=types, spaces=spaces, tools=tools
    )


@bp.route("/about")
# @login_required
def about():
    spaces = Space.query.all()
    tools = Tool.query.all()
    return render_template('default/about.html', spaces=spaces, tools=tools)


@bp.route("/privacy")
# @login_required
def privacy():
    return render_template('default/privacy.html')


@bp.route("/toc")
# @login_required
def toc():
    return render_template('default/toc.html')


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
