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
            for interval in reservation.intervals:
                title = str()
                if reservation.type.name == 'space':
                    title = str(reservation.space.name)
                else:
                    title = str(reservation.tool.name)

                start = interval.calendar.day.strftime(
                    "%Y-%m-%dT") + interval.start_time.strftime("%H:%M:%S")
                end = interval.calendar.day.strftime(
                    "%Y-%m-%dT") + interval.end_time.strftime("%H:%M:%S")
                result.append({
                    "title": title, "id": reservation.id, "type": reservation.type.name,
                    "start": start, "end": end
                })
        return jsonify(result)
