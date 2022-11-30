from flask import jsonify
from flask_login import current_user, login_required

from app.api import bp
from app.models import Reservation


@bp.route('reservations/', methods=['GET'])
@login_required
def get_reservations_data():
    if current_user.role.name == "admin":
        reservations = Reservation.query.all()
        result = []
        for reservation in reservations:
            dates = []
            for cal in reservation.calendars:
                dates.append(cal.day.strftime("%d/%m/%Y, %H:%M:%S"))
            result.append({
                "title": str(reservation.space.name) if reservation.type.name == 'space' else str(reservation.tool.name),
                "dates": dates
            })
        return jsonify(result)
