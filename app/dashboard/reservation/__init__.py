from flask import Blueprint

bp = Blueprint('reservation', __name__, url_prefix="/reservations")

from app.dashboard.reservation import routes