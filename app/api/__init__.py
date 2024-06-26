from flask import Blueprint
from flask_login import login_required
from app.utils import check_is_confirmed

bp = Blueprint('api', __name__, url_prefix="/api")

from app.api import routes


@bp.before_request
@login_required
@check_is_confirmed
def before_request():
    # This function doesn't need to do anything, as it's just a placeholder
    # for the decorators to run.
    pass
