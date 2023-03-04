import itertools
from datetime import datetime

from flask import request, jsonify, abort
from flask_login import current_user, login_required
from sqlalchemy import or_, and_

from app.api import bp
from app.models import (
    Reservation, Tool, Calendar,
    User, CategorySpace, Interval
    # Notification
)


@bp.route('reservations/', methods=['GET'])
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

#
# @bp.route('notifications/', methods=['GET'])
# @login_required
# def notifications():
#     not_read = request.args.get("not_read", type=bool)
#     since = request.args.get("since", 0.0, type=float)
#
#     notifs = Notification.query.\
#         filter(Notification.timestamp > since).\
#         filter(Notification.user_id == current_user.id).\
#         order_by(Notification.timestamp.asc())
#
#     if not_read:
#         notifs.filter(Notification.is_read is None)
#
#     return jsonify([{
#         "id": n.id, "title": n.title, "body": n.body,
#         "datetime": datetime.fromtimestamp(n.timestamp)
#     } for n in notifs])
#
#
# @bp.route('notifications/read/<int:pk>/', methods=['GET'])
# @login_required
# def notifications(pk):
#     notif = Notification.query.get_or_404(pk)
#
#     if notif.user_id != current_user.id:
#         abort(400)
#
#
#     return jsonify([{
#         "id": n.id, "title": n.title, "body": n.body,
#         "datetime": datetime.fromtimestamp(n.timestamp)
#     } for n in notifs])


@bp.route('spaces/', methods=['GET'])
@login_required
def get_spaces():
    user = current_user
    if current_user.role.name == "admin":
        user_id = request.args.get("user_id", type=int)
        if user_id:
            user = User.query.get_or_404(user_id)

    cat_spaces = CategorySpace.query.filter_by(category_id=user.category_id)
    res = list()
    for key, group in itertools.groupby(cat_spaces, lambda x: x.space_id):
        group = list(group)
        res.append({
            "id": key, "name": group[0].space.name,
            "cat_prices": [
                {
                    "id": cat_price.id,
                    "unit_id": cat_price.unit.value,
                    "unit_title": cat_price.unit.description,
                    "unit_value": cat_price.unit_value,
                    "price_id": cat_price.price_unit.value,
                    "price_title": cat_price.price_unit.description,
                    "price_value": cat_price.price,
                } for cat_price in group
            ]
        })

    return jsonify(res)


@bp.route('space/<int:pk>/tools/', methods=['GET'])
@login_required
def get_space_tools(pk):
    tools = [
        {"id": tool.id, "name": tool.name}
        for tool in Tool.query.filter_by(space_id=pk).\
        with_entities(Tool.id, Tool.name).all()
    ]
    return jsonify(tools)


@bp.route('space/<int:pk>/reserved-days/', methods=['POST'])
@login_required
def space_reserved_days(pk):
    data = request.get_json(silent=True)
    if not data:
        abort(400)
    from_time = datetime.strptime(
        data.get("from_time"), '%Y-%m-%dT%H:%M:%S.%fZ'
    ).time()
    to_time = datetime.strptime(
        data.get("to_time"), '%Y-%m-%dT%H:%M:%S.%fZ'
    ).time()

    reserved_days = Calendar.query.\
        join(Calendar.reservations, Calendar.intervals).\
        filter(
            Reservation.space_id == 1,
            or_(
                and_(
                    Interval.start_time < from_time,
                    from_time < Interval.end_time
                ),
                and_(
                    from_time < Interval.start_time,
                    Interval.start_time < to_time
                )
            )
        ).\
        with_entities(Calendar.day).distinct().all()
    return jsonify([cal.day.isoformat() for cal in reserved_days])


