import itertools
from datetime import datetime

from flask import (
    request, redirect, url_for,
    abort, jsonify
)
from flask_login import current_user, login_required

from app import db
from app.api.parser import use_args
from app.api.space import bp
from app.api.space.serializers import space_reservation_args, valid_attendance_num
from app.enums import ReservationTypes, PaymentTypes
from app.models import (
    Tool, Calendar, User, CategorySpace,
    CategoryTool, Space, Reservation, Interval
)


@bp.route('/', methods=['GET'])
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
            "capacity": group[0].space.capacity,
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


@bp.route('/<int:pk>/tools/', methods=['GET'])
@login_required
def get_space_tools(pk):
    user = current_user
    if current_user.role.name == "admin":
        user_id = request.args.get("user_id", type=int)
        if user_id:
            user = User.query.get_or_404(user_id)

    tools = [
        {
            "id": tool.tool_id, "name": tool.name, "cat_id": tool.id,
            "unit_title": tool.unit.description, "price": tool.price,
            "price_title": tool.price_unit.description,
        }
        for tool in CategoryTool.query.join(CategoryTool.tool).filter(
            CategoryTool.category_id == user.category_id,
            Tool.space_id == pk
        ).with_entities(
            Tool.id.label("tool_id"), Tool.name, CategoryTool.id,
            CategoryTool.unit, CategoryTool.price_unit, CategoryTool.price
        ).all()
    ]
    return jsonify(tools)


@bp.route('/<int:pk>/reserved-days/', methods=['POST'])
@login_required
def space_reserved_days(pk):
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
        pk, days_only, from_time, to_time,
    )
    return jsonify([cal.day.isoformat() for cal in reserved_days])


@bp.route('/<int:pk>/calculate-price/', methods=['POST'])
@login_required
def calculate_price(pk):
    user = current_user
    if current_user.role.name == "admin":
        user_id = request.args.get("user_id", type=int)
        if user_id:
            user = User.query.get_or_404(user_id)

    data = request.get_json(silent=True)
    if not data:
        abort(400)

    space = Space.query.get_or_404(pk)
    days = data.get("days", None)
    space_price_id = data.get("space_price_id", None)
    tool_ids = data.get("tool_ids", None)
    space_with_tools = space_price_id and tool_ids
    if not (days and space_price_id):
        abort(400)

    space_cat_price = CategorySpace.query.get_or_404(int(space_price_id))
    total_price = float(days) * space_cat_price.price
    res = [[space.name, total_price, space_cat_price.price_unit.description]]
    tools_total_price = float()
    if space_with_tools:
        tool_ids = [int(tool_id) for tool_id in tool_ids]
        tools_cat_prices = Tool.query.join(Tool.category_prices).filter(
            Tool.id.in_(tool_ids), Tool.space_id == pk,
            CategoryTool.category_id == user.category_id
        ).with_entities(
            Tool.name, CategoryTool.price, CategoryTool.price_unit
        ).all()
        for tool_cat_price in tools_cat_prices:
            res.append([
                tool_cat_price.name, float(days) * tool_cat_price.price,
                tool_cat_price.price_unit.description
            ])
        tools_total_price = sum(
            [float(days) * p.price for p in tools_cat_prices])
    total_price = total_price + tools_total_price
    res.append(["المجموع", total_price])
    return jsonify(res)


@bp.route('/reserve/', methods=['POST'])
@login_required
@use_args(
    space_reservation_args, location="json",
    validate=lambda args: valid_attendance_num(
        args["attendance_num"], args["space_id"]
    )
)
def reserve_space(args):
    home_url = url_for("main.main_page")
    space_reservation_url = url_for(
        "main.reservation.create_reservation_space")
    user = current_user
    status = PaymentTypes.no_payment
    if current_user.role.name == "admin":
        user_id = request.args.get("user_id", type=int)
        home_url = url_for("dashboard.dashboard")
        space_reservation_url = url_for(
            "dashboard.reservation.create_reservation_space")
        status = args.get("payment_status", PaymentTypes.no_payment)
        if user_id:
            user = User.query.get_or_404(user_id)

    space_id = args.get("space_id")
    space = Space.query.get_or_404(space_id)
    days = args.get("days")
    space_price_id = args.get("space_price_id")
    tool_ids = args.get("tools")
    description = args.get("description")
    attendance_num = args.get("attendance_num", None)
    min_age = args.get("min_age", None)
    max_age = args.get("max_age", None)
    from_time = args.get("from_time", None)
    to_time = args.get("to_time", None)
    space_with_tools = space_price_id and tool_ids
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
            space_id, days_only, from_time, to_time,
            days=days, to_reserve=True
    )):
        abort(400)

    space_cat_price = CategorySpace.query.get_or_404(space_price_id)
    days_num = float(len(days))
    tools_total_price = float()

    cals = list()
    tools = list()
    intervals = list()
    if space_with_tools:
        tools_cat_prices = Tool.query.join(Tool.category_prices).filter(
            Tool.id.in_(tool_ids), Tool.space_id == space_id,
            CategoryTool.category_id == user.category_id
        ).with_entities(
            CategoryTool.price
        ).all()
        tools_total_price = sum([days_num * p.price for p in tools_cat_prices])

        tools = Tool.query.filter(
            Tool.id.in_(tool_ids), Tool.space_id == space_id
        ).all()
    total_price = days_num * space_cat_price.price + tools_total_price

    reservation = Reservation(
        type=ReservationTypes.space, payment_status=status, min_age=min_age,
        max_age=max_age, space=space, full_price=total_price, user=user,
        description=description, attendance_num=attendance_num
    )

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

    reservation.tools = tools
    reservation.calendars = cals
    reservation.intervals = intervals
    db.session.add(reservation)
    db.session.commit()
    return jsonify({
        "status": "OK",
        "message": f"تم حجز المساحة",
        "home_url": home_url,
        "space_reservation_url": space_reservation_url
    })
