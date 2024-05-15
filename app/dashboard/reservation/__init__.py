from flask import Blueprint

bp = Blueprint('reservation', __name__, url_prefix="/reservation")

from app.dashboard.reservation import routes
