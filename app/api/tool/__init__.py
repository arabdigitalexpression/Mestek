from flask import Blueprint

bp = Blueprint('tool', __name__, url_prefix="/tools")

from app.api.tool import routes
