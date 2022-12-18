from flask import (
    render_template, redirect, url_for, flash, )
from flask_login import current_user, login_required

from app import db
from app.main.profile import bp
from app.main.profile.forms import EditUserForm, ChangePasswordForm
from app.utils import save_file, remove_file


@bp.route('/')
@login_required
def profile():
    return render_template("profile/general_info.html")


@bp.route('/reservations')
@login_required
def profile_reservation():
    return render_template("profile/reservations.html")


@bp.route('/edit', methods=["GET", "POST"])
@login_required
def profile_edit():
    form = EditUserForm()
    if form.validate_on_submit():
        current_user.first_name = form.firstName.data
        current_user.last_name = form.lastName.data
        current_user.username = form.userName.data
        current_user.email = form.email.data
        current_user.phone = form.phone.data
        current_user.address = form.address.data
        current_user.website_url = form.website_url.data
        current_user.gender = form.gender.data
        current_user.birthday = form.birthday.data
        if current_user.avatar_url:
            remove_file("user", current_user.avatar_url.split("/")[-1])
        if form.avatar_url.data:
            current_user.avatar_url = save_file("user", form.avatar_url.data)
        db.session.commit()
        return redirect(url_for("main.profile.profile"))
    form.firstName.data = current_user.first_name
    form.lastName.data = current_user.last_name
    form.userName.data = current_user.username
    form.email.data = current_user.email
    form.phone.data = current_user.phone
    form.address.data = current_user.address
    form.website_url.data = current_user.website_url
    form.gender.data = current_user.gender.name
    form.birthday.data = current_user.birthday
    form.avatar_url.data = current_user.avatar_url
    return render_template("profile/update_profile.html", form=form)


@bp.route('/change-password', methods=["GET", "POST"])
@login_required
def change_password():
    form = ChangePasswordForm()

    current_pass = form.current_password.data

    if form.validate_on_submit():
        if not current_user.verify_password(current_pass):
            flash("كلمة المرور الحالية غير صحيحة", "error")
            return render_template("profile/change_password.html", form=form)
        if not form.password.data == form.confirm_password.data:
            flash("كلمة المرور غير مطابقة", "error")
            return render_template("profile/change_password.html", form=form)
        current_user.make_password(form.password.data)
        db.session.commit()
        flash("تم تعيين كلمة مرور جديدة بنجاح", "info")
        return redirect(url_for("main.profile.profile"))
    return render_template("profile/change_password.html", form=form)
