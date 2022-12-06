from flask import (
    render_template, request, redirect,
    url_for, flash
)
from flask_login import current_user, login_required

from app import db
from app.dashboard.forms import ConfirmForm
from app.dashboard.user import bp
from app.dashboard.user.forms import UserCreateForm, ChangePasswordForm
from app.models import User, Category, Role


@bp.route('/')
@login_required
def user_list():
    data = User.query.all()
    form = ConfirmForm()
    if current_user.role.name == "admin":
        return render_template('dashboard/user/index.html', current_user=current_user, form=form, users=data)
    else:
        return render_template("dashboard/index.html")


@bp.route('/<string:username>')
@login_required
def get_user(username):
    user = User.query.filter_by(username=username).first_or_404()
    if current_user.role.name == "admin":
        return render_template('dashboard/user/profile.html', user=user)
    else:
        return render_template("dashboard/index.html")


@bp.route('/<string:username>/delete', methods=['POST'])
@login_required
def delete_user(username):
    form = ConfirmForm()
    if form.validate_on_submit() and form.value.data == username:
        user = User.query.filter_by(username=username).first_or_404()
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for("dashboard.user.user_list"))


@bp.route('/create', methods=["GET", "POST"])
@login_required
def create_user():
    categories = Category.query.all()
    roles = Role.query.all()
    form = UserCreateForm()
    form.category.choices = [(c.id, c.name) for c in categories]
    form.category.choices.insert(0, (0, "-- اختر تصنيف --"))
    form.role.choices = [(r.id, r.name) for r in roles]
    form.role.choices.insert(0, (0, "-- اختر صلاحية --"))
    if request.method == "POST":
        if form.validate_on_submit():
            first_name = form.firstName.data
            last_name = form.lastName.data
            username = form.userName.data
            email = form.email.data
            password = form.password.data
            role = form.role.data
            category = form.category.data
            user = User.query.get(email)
            if user is None:
                user = User(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    email=email,
                    role=Role.query.get(role) if not role == 0 else None,
                    category=Category.query.get(
                        category) if not category == 0 else None
                )

                user.make_password(password)
                user.save()
                return redirect(url_for("dashboard.user.user_list"))
            # TODO: there's a logic error here, fix it!
            errors = f"hey, There's a user with this email: {email}"
            # render_template does autoescaping html form input data
            return render_template("dashboard/user/form.html", form=form, errors=errors)
        errors = f"Please check your form data again"
        return render_template("dashboard/user/form.html", form=form, errors=errors)
    return render_template("dashboard/user/form.html", form=form)


@bp.route('/<string:username>/update', methods=["GET", "POST"])
@login_required
def update_user(username):
    if current_user.role.name == "admin":
        categories = Category.query.all()
        roles = Role.query.all()
        form_user = UserCreateForm()
        form_password = ChangePasswordForm()
        form_user.category.choices = [(c.id, c.name) for c in categories]
        form_user.category.choices.insert(0, (0, "-- اختر تصنيف --"))
        form_user.role.choices = [(r.id, r.name) for r in roles]
        form_user.role.choices.insert(0, (0, "-- اختر صلاحية --"))
        user = User.query.filter_by(username=username).first_or_404()
        if request.method == "GET":
            form_user.firstName.data = user.first_name
            form_user.lastName.data = user.last_name
            form_user.userName.data = user.username
            form_user.email.data = user.email
            form_user.phone.data = user.phone
            form_user.address.data = user.address
            form_user.website_url.data = user.website_url
            form_user.gender.data = user.gender.name
            form_user.birthday.data = user.birthday
            form_user.avatar_url.data = user.avatar_url
            form_user.role.data = str(
                user.role.id) if not user.role == None else "0"
            form_user.category.data = str(
                user.category.id) if not user.category == None else "0"
            return render_template(
                'dashboard/user/form.html',
                form_user=form_user, form_password=form_password, isUpdate=True, user=user
            )
        elif request.method == "POST":
            user.first_name = form_user.firstName.data
            user.last_name = form_user.lastName.data
            user.username = form_user.userName.data
            user.email = form_user.email.data
            user.address = form_user.address.data
            user.website_url = form_user.website_url.data
            user.gender = form_user.gender.data
            user.birthday = form_user.birthday.data
            user.avatar_url = form_user.avatar_url.data
            user.role = Role.query.get(
                form_user.role.data) if not form_user.role.data == 0 else None
            user.category = Category.query.get(
                form_user.category.data) if not form_user.category.data == 0 else None
            db.session.commit()
            return redirect(url_for("dashboard.user.user_list"))
    else:
        return redirect(url_for("main.main_page"))


@bp.route('/<string:username>//change-password', methods=["GET", "POST"])
@login_required
def change_password(username):
    form = ChangePasswordForm()
    user = User.query.filter_by(username=username).first_or_404()
    if form.validate_on_submit():
        if not form.password.data == form.confirm_password.data:
            flash("كلمة المرور غير مطابقة", "error")
            return redirect(url_for("dashboard.user.update_user", username=user.username))
        user.make_password(form.password.data)
        db.session.commit()
        flash("تم تعيين كلمة مرور جديدة بنجاح", "info")
        return redirect(url_for("dashboard.user.update_user", username=user.username))
    return redirect(url_for("dashboard.user.update_user", username=user.username))