import datetime
import math

from flask import (
    jsonify, abort, redirect, url_for, request,
)
from flask_login import current_user, login_required

from app import db
from app.api.reservation import bp
from app.models import (
    Reservation, Space, Tool, User,
    Calendar, Interval
)


@bp.route('/', methods=['GET'])
@login_required
def get_reservations_data():
    if current_user.role.name == "admin":
        reservations = Reservation.query.all()
        result = []
        for reservation in reservations:
            dates = []
            for cal in reservation.calendars:
                dates.append(cal.day)

            if not dates:
                continue

            data = {
                "title": str(reservation.space.name) if reservation.type.name == 'space' else str(
                    reservation.tool.name),
                "start": min(dates).strftime("%Y-%m-%dT%H:%M:%S"),
                # "dates": dates
            }
            if len(dates) > 1:
                data["end"] = max(dates).strftime("%Y-%m-%dT%H:%M:%S")
            result.append(data)
        return jsonify(result)
