from flask import Blueprint

bp = Blueprint('category', __name__, url_prefix="/categories")

from app.dashboard.category import routes
