import itertools
from datetime import datetime

from flask import (
    request, redirect, url_for,
    abort, jsonify
)
from flask_login import current_user, login_required

from app import db
from app.api.parser import use_args
from app.api.tool import bp
from app.api.tool.serializers import tool_reservation_args
from app.enums import ReservationTypes, PaymentTypes
from app.models import (
    Tool, Calendar, User, CategoryTool,
    Reservation, Interval
)


@bp.route('/', methods=['GET'])
@login_required
def get_tools():
    user = current_user
    if current_user.role.name == "admin":
        user_id = request.args.get("user_id", type=int)
        if user_id:
            user = User.query.get_or_404(user_id)

    cat_tools = CategoryTool.query.join(
        CategoryTool.tool
    ).filter(
        CategoryTool.category_id == user.category_id,
        Tool.space_id == None
    ).all()
    res = list()
    for key, group in itertools.groupby(cat_tools, lambda x: x.tool_id):
        group = list(group)
        res.append({
            "id": key, "name": group[0].tool.name,
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


@bp.route('/<int:pk>/reserved-days/', methods=['POST'])
@login_required
def tool_reserved_days(pk):
    data = request.get_json(silent=True)
    if not data:
        abort(400)
    days_only = data.get("days_only", None)
    from_time = data.get("from_time", None)
    to_time = data.get("to_time", None)
    if not days_only and from_time and to_time:
        from_time = datetime.strptime(
            from_time, '%Y-%m-%dT%H:%M:%S.%fZ'
        ).time()
        to_time = datetime.strptime(
            to_time, '%Y-%m-%dT%H:%M:%S.%fZ'
        ).time()
        # TODO: replace hardcoded time with app config settings
        org_day_start = 10
        org_day_end = 19
        if from_time.hour < org_day_start or to_time.hour > org_day_end:
            abort(400)

    reserved_days = Calendar.reserved_days(
        pk, days_only, from_time, to_time, space=False
    )
    return jsonify([cal.day.isoformat() for cal in reserved_days])


@bp.route('/<int:pk>/calculate-price/', methods=['POST'])
@login_required
def calculate_price(pk):
    data = request.get_json(silent=True)
    if not data:
        abort(400)

    tool = Tool.query.get_or_404(pk)
    days = data.get("days", None)
    tool_price_id = data.get("tool_price_id", None)
    if not (days and tool_price_id):
        abort(400)

    tool_cat_price = CategoryTool.query.get_or_404(int(tool_price_id))
    total_price = float(days) * tool_cat_price.price
    res = [[tool.name, total_price, tool_cat_price.price_unit.description]]
    res.append(["المجموع", total_price])
    return jsonify(res)


@bp.route('/reserve/', methods=['POST'])
@login_required
@use_args(tool_reservation_args, location="json")
def reserve_tool(args):
    home_url = url_for("main.main_page")
    tool_reservation_url = url_for("main.reservation.create_reservation_tool")
    user = current_user
    status = PaymentTypes.no_payment
    if current_user.role.name == "admin":
        tool_reservation_url = url_for(
            "dashboard.reservation.create_reservation_tool")
        user_id = request.args.get("user_id", type=int)
        home_url = url_for("dashboard.dashboard")
        status = args.get("payment_status", PaymentTypes.no_payment)
        if user_id:
            user = User.query.get_or_404(user_id)

    tool_id = args.get("tool_id")
    tool = Tool.query.get_or_404(tool_id)
    days = args.get("days")
    tool_price_id = args.get("tool_price_id")
    description = args.get("description")
    from_time = args.get("from_time", None)
    to_time = args.get("to_time", None)
    days_only = args.get("days_only") and not (from_time and to_time)
    # TODO: replace hardcoded time with app config settings
    org_day_start = 10
    org_day_end = 19
    now = datetime.now()
    if not days_only:
        from_time = from_time.time()
        to_time = to_time.time()
        if from_time.hour < org_day_start or to_time.hour > org_day_end:
            abort(400)
    if any(Calendar.reserved_days(
            tool_id, days_only, from_time, to_time,
            days=days, to_reserve=True, space=False
    )):
        abort(400)

    tool_cat_price = CategoryTool.query.get_or_404(tool_price_id)
    days_num = float(len(days))

    cals = list()
    intervals = list()
    total_price = days_num * tool_cat_price.price

    reservation = Reservation(
        type=ReservationTypes.tool, payment_status=status, user=user,
        tool=tool, full_price=total_price, description=description,
    )
    print(days)
    for day in days:
        cal = Calendar.query.filter_by(day=day).first()
        if not days_only:
            interval = Interval(start_time=from_time, end_time=to_time)
        else:
            interval = Interval(
                start_time=now.replace(
                    hour=org_day_start, minute=0, second=0, microsecond=0
                ).time(),
                end_time=now.replace(
                    hour=org_day_end, minute=0, second=0, microsecond=0
                ).time()
            )
        if not cal:
            cale = Calendar(day=day, intervals=list())
            cale.intervals.append(interval)
            db.session.add(cale)
            cals.append(cale)
        else:
            cal.intervals.append(interval)
            cals.append(cal)
        intervals.append(interval)

    reservation.calendars = cals
    reservation.intervals = intervals
    db.session.add(reservation)
    db.session.commit()
    return jsonify({
        "status": "OK",
        "message": f"تم حجز الأداة",
        "home_url": home_url,
        "tool_reservation_url": tool_reservation_url
    })
