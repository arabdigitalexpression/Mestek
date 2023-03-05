from flask import Blueprint

bp = Blueprint('reservation', __name__, url_prefix="/reservations")

from app.api.reservation import routes
