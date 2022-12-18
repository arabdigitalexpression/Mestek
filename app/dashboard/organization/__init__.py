from flask import Blueprint

bp = Blueprint('organization', __name__, url_prefix="/organizations")

from app.dashboard.organization import routes
