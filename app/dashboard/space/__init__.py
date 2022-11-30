from flask import Blueprint

bp = Blueprint('space', __name__, url_prefix="/spaces")

from app.dashboard.space import routes