import math

from flask import (
    render_template, request, redirect,
    url_for
)
from flask_login import current_user, login_required

from app import db, connection
from werkzeug.utils import secure_filename
from app import app, db
from app.models import Space, Tool, Image, Category, CategorySpace
from app.enums import SpaceUnit, PriceUnit
from app.dashboard.space import bp
from app.dashboard.space.forms import SpaceForm
from app.models import Space, Tool, Image, Category
from app.utils import save_file


@bp.route('/', methods=["GET", "POST"])
@login_required
def space_list():
    if current_user.role.name == "admin":
        data = Space.query.all()
        return render_template('dashboard/space/index.html', spaces=data)


@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete_space(id):
    if current_user.role.name == "admin":
        space = Space.query.get(id)
        tools = Tool.query.filter_by(space_id=id)
        images = Image.query.filter_by(space_id=id)
        for tool in tools:
            tool.space_id = None
        for image in images:
            db.session.delete(image)
        for cat_price in space.category_prices:
            db.session.delete(cat_price)
        db.session.delete(space)
        db.session.commit()
        return redirect(url_for("dashboard.space.space_list"))
    else:
        return redirect(url_for("main.main_page"))


@bp.route("/create", methods=["GET", "POST"])
@login_required
def create_space():
    form = SpaceForm()
    categories = Category.query.all()
    if current_user.role.name == "admin":
        if form.validate_on_submit() and not form.add_new_price.data:
            space = Space(
                name=form.name.data,
                has_operator=form.has_operator.data,
                description=form.description.data,
                guidelines=form.guidelines.data,
                capacity=form.capacity.data,
            )
            space.set_category_prices(
                form.category_prices.data, categories
            )
            imagesObjs = list()
            for file in form.images.data:
                if not file:
                    continue
                url = save_file("space", file)
                imagesObjs.append(Image(url=url))
            space.images = imagesObjs
            db.session.add(space)
            db.session.commit()
            return redirect(url_for("dashboard.space.space_list"))
        cat_prices = [
            {"category_id": cat.id}
            for cat in categories
        ]
        form.category_prices.append_entry({"price_list": cat_prices})
        return render_template("dashboard/space/form.html", form=form, categories=categories)
    else:
        return redirect(url_for("main.main_page"))


@bp.route("/<int:id>/update", methods=["GET", "POST"])
@login_required
def update_space(id):
    if current_user.role.name == "admin":
        form = SpaceForm()
        space = Space.query.get(id)
        categories = Category.query.all()
        if request.method == "GET":
            form.name.data = space.name
            form.capacity.data = space.capacity
            form.images.data = space.images
            form.guidelines.data = space.guidelines
            form.description.data = space.description
            form.has_operator.data = space.has_operator

            form.process_cat_prices(space.get_category_prices())
            return render_template(
                'dashboard/space/form.html',
                form=form, isUpdate=True, space=space, categories=categories
            )
        elif request.method == "POST":
            if form.validate_on_submit() and not form.add_new_price.data:
                space.name = form.name.data
                space.has_operator = form.has_operator.data
                space.description = form.description.data
                space.guidelines = form.guidelines.data
                space.capacity = form.capacity.data

                for cat_price in space.category_prices:
                    db.session.delete(cat_price)
                db.session.commit()
                space.set_category_prices(
                    form.category_prices.data, categories
                )

                imagesObjs = list()
                for file in form.images.data:
                    if not file:
                        continue
                    url = save_file("space", file)
                    imagesObjs.append(Image(url=url))
                db.session.add_all(imagesObjs)
                db.session.commit()
                return redirect(url_for("dashboard.space.space_list"))
            if form.validate_on_submit() and form.add_new_price.data:
                cat_prices = [
                    {"category_id": cat.id}
                    for cat in categories
                ]
                form.category_prices.append_entry({"price_list": cat_prices})
            return render_template(
                "dashboard/space/form.html",
                form=form, isUpdate=True, space=space, categories=categories
            )
    else:
        return redirect(url_for("main.main_page"))
