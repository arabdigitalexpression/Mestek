from flask import Blueprint

bp = Blueprint('tool', __name__, url_prefix="/tools")

from app.dashboard.tool import routes