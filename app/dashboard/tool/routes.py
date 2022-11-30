import os
import math
from uuid import uuid1

from flask import (
    render_template, request, redirect,
    url_for
)
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from app import app, db, connection
from app.models import Space, Tool, Image, Category, CategoryTool
from app.enums import ToolUnit, PriceUnit
from app.dashboard.tool import bp
from app.dashboard.tool.forms import ToolForm


@bp.route('/', methods=["GET", "POST"])
@login_required
def tool_list():
    i = 1
    j = 10
    if current_user.role.name == "admin":
        data = Tool.query.all()
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM tool")
        data2 = cursor.fetchone()
        rows = data2['COUNT(*)']
        if rows % 10 == 0:
            pages = rows/10
        else:
            pages = math.trunc(rows/10)+1
        if request.method == 'POST':
            if request.form.get("b") != None:
                num = int(request.form.get("b"))
                global x
                x = int(request.form.get("b"))
                i = int(str(num-1) + "1")
                j = int(str(num) + "0")
            elif request.form.get("next") == "next":
                try:
                    x
                except NameError:
                    x = 1
                x += 1
                print(pages)
                print(x)

                if x >= pages:
                    x = pages
                i = int(str(x-1) + "1")
                j = int(str(x) + "0")

            elif request.form.get("Previous") == "Previous":
                try:
                    x
                except NameError:
                    x = 1
                x -= 1
                if x <= 0:
                    x = 1
                i = int(str(x-1) + "1")
                j = int(str(x) + "0")
        return render_template('dashboard/tool/index.html', tools=data, i=i, j=j, pages=pages)


@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete_tool(id):
    if current_user.role.name == "admin":
        tool = Tool.query.get(id)
        images = Image.query.filter_by(tool_id=id)
        for image in images:
            db.session.delete(image)
        db.session.delete(tool)
        db.session.commit()
        return redirect(url_for("dashboard.tool.tool_list"))
    else:
        return redirect(url_for("main.main_page"))


@bp.route("/create", methods=["GET", "POST"])
@login_required
def create_tool():
    spaces = Space.query.all()
    form = ToolForm()
    categories = Category.query.all()
    form.space.choices = [(s.id, s.name) for s in spaces]
    form.space.choices.insert(0, (0, "-- اختر المساحة --"))
    if current_user.role.name == "admin":
        if form.validate_on_submit() and not form.add_new_price.data:
            tool = Tool(
                name=form.name.data,
                has_operator=form.has_operator.data,
                description=form.description.data,
                guidelines=form.guidelines.data,
                quantity=form.quantity.data,
                space=Space.query.get(
                    form.space.data) if not form.space.data == 0 else None
            )
            for cat_price in form.category_prices.data:
                for price in cat_price["price_list"]:
                    category = next(filter(
                        lambda cat: cat.id == int(price["category_id"]),
                        categories
                    ), None)
                    tool.category_prices.append(CategoryTool(
                        unit_value=float(cat_price["unit_value"]),
                        unit=ToolUnit[cat_price["unit"].split('.')[1]],
                        price=float(price["price"]),
                        price_unit=PriceUnit[price["price_unit"].split('.')[
                            1]],
                        category=category
                    ))
            imagesObjs = list()
            for file in form.images.data:
                if not file:
                    continue
                filename = str(uuid1()) + "-" + secure_filename(file.filename)
                file.save(os.path.join(
                    app.config["APP_PATH"],
                    app.config["UPLOAD_PATH"],
                    "tool",
                    filename
                ))
                imagesObjs.append(Image(
                    url=url_for(
                        "main.download_file",
                        dir="tool",
                        filename=filename
                    )
                ))
            tool.images = imagesObjs
            db.session.add(tool)
            db.session.commit()
            return redirect(url_for("dashboard.tool.tool_list"))
        cat_prices = [
            {"category_id": cat.id}
            for cat in categories
        ]
        if request.method == "POST" and form.add_new_price.data:
            form.category_prices.append_entry({"price_list": cat_prices})
            return render_template("dashboard/tool/form.html", form=form, categories=categories)
        form.process(data={
            "category_prices": [
                {
                    "price_list": cat_prices
                }
            ]
        })
        return render_template("dashboard/tool/form.html", form=form, categories=categories)
    else:
        return redirect(url_for("main.main_page"))


@bp.route("/<int:id>/update", methods=["GET", "POST"])
@login_required
def update_tool(id):
    if current_user.role.name == "admin":
        spaces = Space.query.all()
        form = ToolForm()
        form.space.choices = [(s.id, s.name) for s in spaces]
        form.space.choices.insert(0, (0, "-- اختر المساحة --"))
        tool = Tool.query.get(id)
        if request.method == "GET":
            form.name.data = tool.name
            form.quantity.data = tool.quantity
            form.images.data = tool.images
            form.guidelines.data = tool.guidelines
            form.description.data = tool.description
            form.has_operator.data = tool.has_operator
            form.space.data = str(
                tool.space.id) if not tool.space == None else "0"
            return render_template(
                'dashboard/tool/form.html',
                form=form, isUpdate=True, tool=tool
            )
        elif request.method == "POST":
            if form.validate_on_submit():
                tool.name = form.name.data
                tool.has_operator = form.has_operator.data
                tool.description = form.description.data
                tool.guidelines = form.guidelines.data
                tool.quantity = form.quantity.data
                tool.space = Space.query.get(
                    form.space.data) if not form.space.data == 0 else None
                imagesObjs = list()
                for file in form.images.data:
                    if not file:
                        continue
                    filename = str(uuid1()) + "-" + \
                               secure_filename(file.filename)

                    # TODO: image is overwritten when there's
                    # an existing image with the same name
                    file.save(os.path.join(
                        app.config["APP_PATH"],
                        app.config["UPLOAD_PATH"],
                        "tool",
                        filename
                    ))
                    imagesObjs.append(Image(
                        tool=tool,
                        url=url_for(
                            "main.download_file",
                            dir="tool",
                            filename=filename
                        )
                    ))
                db.session.add_all(imagesObjs)
                db.session.commit()
                return redirect(url_for("dashboard.tool.tool_list"))
            return render_template(
                "dashboard/tool/form.html",
                form=form, isUpdate=True, tool=tool
            )
    else:
        return redirect(url_for("main.main_page"))
