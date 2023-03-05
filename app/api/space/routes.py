import itertools
from datetime import datetime

from flask import (
    request, redirect, url_for,
    abort, jsonify
)
from flask_login import current_user, login_required

from app.api.space import bp
from app.models import (
    Tool, Calendar, User, CategorySpace,
    CategoryTool, Space
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
    days = data.get("days", None)
    from_time = data.get("from_time", None)
    to_time = data.get("to_time", None)
    if days_only:
        days = [
            datetime.strptime(day, '%Y-%m-%dT%H:%M:%S.%fZ').date()
            for day in days
        ]
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

    reserved_days = Calendar.space_reserved_days(
        pk, days_only, days, from_time, to_time
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
    res = [[space.name, space_cat_price.price]]
    tools_total_price = float()
    if space_with_tools:
        tool_ids = [int(tool_id) for tool_id in tool_ids]
        tools_cat_prices = Tool.query.join(Tool.category_prices).filter(
            Tool.id.in_(tool_ids), Tool.space_id == pk,
            CategoryTool.category_id == user.category_id
        ).with_entities(
            Tool.name, CategoryTool.price
        ).all()
        for tool_cat_price in tools_cat_prices:
            res.append([tool_cat_price.name, tool_cat_price.price])
        tools_total_price = sum([float(days) * p.price for p in tools_cat_prices])
    total_price = float(days) * space_cat_price.price + tools_total_price
    res.append(["المجموع", total_price])
    return jsonify(res)
