from flask import (
    render_template, request, redirect,
    url_for
)
from flask_login import current_user, login_required

from app import db
from app.models import Role, User
from app.dashboard.role import bp
from app.dashboard.forms import ConfirmForm, RoleCategoryForm


@bp.route('/', methods=["GET", "POST"])
@login_required
def get_roles():
    roles = Role.query.all()
    form = RoleCategoryForm()
    input = ConfirmForm()
    if current_user.role.name == "admin":
        if request.method == "POST":
            if form.validate_on_submit():
                name = form.name.data
                color_code = form.colorCode.data
                role = Role.query.get(name)

                if role == None:
                    role = Role(
                        name=name,
                        color_code=color_code,
                    )
                    db.session.add(role)
                    db.session.commit()
                    roles = Role.query.all()
                errors = f"hey, There's a role with this name: {name}"
                return render_template("dashboard/user/role/index.html", form=form, errors=errors, roles=roles, input=input)
            errors = f"Please check your form data again"
            return render_template("dashboard/user/role/index.html", form=form, errors=errors, roles=roles, input=input)
        return render_template("dashboard/user/role/index.html", form=form, roles=roles, input=input)
    else:
        return redirect(url_for("main.main_page"))

@bp.route('<int:id>/update', methods=["GET", "POST"])
@login_required
def update_role(id):
    input = ConfirmForm()
    role = Role.query.get(id)
    if current_user.role.name == "admin":
        form = RoleCategoryForm()
        if request.method == "GET":
            roles = Role.query.all()
            form.name.data = role.name
            form.colorCode.data = role.color_code
            return render_template(
                'dashboard/user/role/index.html',
                form=form, isUpdate=True, roles=roles, role=role, input=input
            )
        elif request.method == "POST":
            roles = Role.query.all()
            if form.validate_on_submit():
                role.name = form.name.data
                role.color_code = form.colorCode.data

                db.session.commit()
                return redirect(url_for("dashboard.role.get_roles"))
            return render_template(
                "dashboard/user/role/index.html",
                form=form, isUpdate=True, roles=roles, input=input
            )
    else:
        return redirect(url_for("main.main_page"))


@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete_role(id):
    if current_user.role.name == "admin":
        input = ConfirmForm()
        role = Role.query.get(id)
        if input.validate_on_submit() and input.value.data == role.name:
            users = User.query.filter_by(role_id=id)
            for user in users:
                db.session.delete(user)
            db.session.delete(role)
            db.session.commit()
            return redirect(url_for("dashboard.role.get_roles"))
    else:
        return redirect(url_for("main.main_page"))
