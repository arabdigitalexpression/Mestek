from flask import (
    render_template, request, redirect,
    url_for
)
from flask_login import current_user, login_required

from app import db
from app.dashboard.category import bp
from app.dashboard.forms import ConfirmForm, RoleCategoryForm
from app.models import Category, User
from app.random_color import generate_color


@bp.route('/', methods=["GET", "POST"])
@login_required
def get_categories():
    categories = Category.query.all()
    form = RoleCategoryForm()
    input = ConfirmForm()
    if current_user.role.name == "admin":
        if request.method == "POST":
            if form.validate_on_submit():
                name = form.name.data
                description = form.desc.data
                color_code = form.colorCode.data
                is_organization = form.isOrganization.data
                category = Category.query.get(name)
                if category == None:
                    category = Category(
                        name=name,
                        description=description,
                        color_code=color_code,
                        is_organization=is_organization,
                    )
                    db.session.add(category)
                    db.session.commit()
                    categories = Category.query.all()
                errors = f"hey, There's a category with this name: {name}"
                return render_template("dashboard/user/category/index.html", form=form, errors=errors,
                                       categories=categories, input=input)
            errors = f"Please check your form data again"
            return render_template("dashboard/user/category/index.html", form=form, errors=errors,
                                   categories=categories, input=input)
        form.colorCode.data = generate_color()
        return render_template("dashboard/user/category/index.html", form=form, categories=categories, input=input)
    else:
        return redirect(url_for('main.main_page'))


@bp.route('/<int:id>/update', methods=["GET", "POST"])
@login_required
def update_category(id):
    input = ConfirmForm()
    category = Category.query.get(id)
    if current_user.role.name == "admin":
        form = RoleCategoryForm()
        if request.method == "GET":
            categories = Category.query.all()
            form.name.data = category.name
            form.desc.data = category.description
            form.colorCode.data = category.color_code
            form.isOrganization.data = category.is_organization
            return render_template(
                'dashboard/user/category/index.html',
                form=form, isUpdate=True, categories=categories, category=category, input=input
            )
        elif request.method == "POST":
            categories = Category.query.all()
            if form.validate_on_submit():
                category.name = form.name.data
                category.description = form.desc.data
                category.color_code = form.colorCode.data
                category.is_organization = form.isOrganization.data
                db.session.commit()
                return redirect(url_for("dashboard.category.get_categories"))
            return render_template(
                "dashboard/user/category/index.html",
                form=form, isUpdate=True, categories=categories, input=input
            )
    else:
        return redirect(url_for('main.main_page'))


@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete_category(id):
    if current_user.role.name == "admin":
        input = ConfirmForm()
        category = Category.query.get(id)
        if input.validate_on_submit() and input.value.data == category.name:
            users = User.query.filter_by(category_id=id).all()
            for user in users:
                db.session.delete(user)
            for cat_price in category.category_prices:
                db.session.delete(cat_price)
            db.session.delete(category)
            db.session.commit()
            return redirect(url_for("dashboard.category.get_categories"))
    else:
        return redirect(url_for('main.main_page'))
