from flask import (
    render_template, request, redirect,
    url_for, current_app, flash
)
from flask_login import current_user, login_user, logout_user, login_required

from app import db
from app.auth import bp
from app.auth.forms import SignupForm, LoginForm
from app.models import (
    Category, Role, User
)
from app.utils import send_confirmation, confirm_token


@bp.route("/signup", methods=["GET", "POST"])
def signup_page():
    if current_user.is_authenticated:
        if current_user.role.name == 'admin':
            return redirect(url_for("dashboard.dashboard"))
        elif current_user.role.name == 'user':
            return redirect(url_for("main.main_page"))

    form = SignupForm()
    categories = Category.query.all()
    form.category.choices = [(c.id, c.name) for c in categories]
    form.category.choices.insert(0, ("", "-- اختر تصنيف --"))

    if form.validate_on_submit():
        username = form.userName.data
        email = form.email.data

        user = User.query.filter((User.email == email) | (User.username == username)).first()
        if user:
            flash('An account already exists with this username or email.', 'error')
            return render_template("auth/signup.html", form=form)

        user = User(
            first_name=form.firstName.data,
            last_name=form.lastName.data,
            username=username,
            phone=form.phone.data,
            email=email,
            gender=form.gender.data,
            role=Role.query.get(2),  # Assuming role with ID 2 is 'user'
            category=Category.query.get(form.category.data)
        )
        user.make_password(form.password.data)
        user.save()

        status_code, response = send_confirmation(user.email, user.full_name)
        if status_code == 200:
            flash("تم إرسال رسالة تأكيد بالبريد الإلكتروني عبر البريد الإلكتروني.", "success")
            return redirect(url_for("auth.login_page"))
        else:
            current_app.logger.error("Failed to send confirmation email")
            flash("حدث خطأ أثناء إرسال رسالة التأكيد الإلكترونية.", "danger")
            return redirect(url_for("auth.login_page"))
    return render_template("auth/signup.html", form=form)


@bp.route("/login", methods=["GET", "POST"])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for("main.main_page"))

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # user = User.query.get()
        # filter users by username and then get first one
        user = User.query.filter_by(username=username).first()

        if user is None:
            msg = "إسم المستخدم أو كلمة المرور غير صحيحة"
            # render_template does autoescaping html form input data
            return render_template("auth/login.html", form=form, msg=msg)

        if not user.verify_password(password):
            msg = "إسم المستخدم أو كلمة المرور غير صحيحة"
            # render_template does autoescaping html form input data
            return render_template("auth/login.html", form=form, msg=msg)

        # remember the user when he visits other pages
        # TODO: add remember me button to the form
        login_user(user, remember=True)
        if current_user.role.name == "admin":
            return redirect(url_for("dashboard.dashboard"))
        else:
            return redirect(url_for("main.main_page"))
    return render_template("auth/login.html", form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.main_page'))


@bp.route('/confirm/<token>')
def confirm_email(token):
    email = confirm_token(token)
    if not email:
        flash("رابط التأكيد غير صالح أو انتهت صلاحيته.", "danger")
        return redirect(url_for('auth.login_page'))
    user = User.query.filter_by(email=email).first_or_404()
    if user.activated:
        flash("لقد تم بالفعل تأكيد حسابك.", "success")
        return redirect(url_for("main.main_page"))

    user.activated = True
    db.session.add(user)
    db.session.commit()
    login_user(user, remember=True)
    flash("لقد أكدت حسابك. شكرًا!", "success")
    return redirect(url_for('main.main_page'))


@bp.route("/inactive")
@login_required
def inactive():
    if current_user.activated:
        return redirect(url_for("main.main_page"))
    return render_template("profile/inactive.html")



@bp.route("/resend")
@login_required
def resend_confirmation():
    if current_user.activated:
        flash("لقد تم بالفعل تأكيد حسابك.", "success")
        return redirect(url_for("main.main_page"))
    send_confirmation(current_user.email, current_user.full_name)
    flash("تم إرسال رسالة تأكيد جديدة بالبريد الإلكتروني.", "success")
    return redirect(url_for("auth.inactive"))
