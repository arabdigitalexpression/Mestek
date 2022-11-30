from flask import Blueprint

bp = Blueprint('reservation', __name__, url_prefix="/reservations")

from app.main.reservation import routes
