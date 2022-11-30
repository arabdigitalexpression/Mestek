from flask import Blueprint

bp = Blueprint('profile', __name__, url_prefix="/profile")

from app.main.profile import routes
