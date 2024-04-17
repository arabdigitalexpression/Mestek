from flask import Blueprint
from app.utils import check_is_confirmed

bp = Blueprint('main', __name__)

from app.main import routes


@bp.before_request
@check_is_confirmed
def before_request():
    # This function doesn't need to do anything, as it's just a placeholder
    # for the decorators to run.
    pass
