from flask import Blueprint

bp = Blueprint('role', __name__, url_prefix="/roles")

from app.dashboard.role import routes
