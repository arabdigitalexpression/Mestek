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
    if current_user.is_authenticated and current_user.role.name == 'admin':
        return redirect(url_for("dashboard.dashboard"))
    elif current_user.is_authenticated and current_user.role.name == 'user':
        return redirect(url_for("main.main_page"))
    form = SignupForm()
    categories = Category.query.all()
    form.category.choices = [(c.id, c.name) for c in categories]
    form.category.choices.insert(0, ("", "-- اختر تصنيف --"))
    if request.method == "POST":
        if form.validate_on_submit():
            first_name = form.firstName.data
            last_name = form.lastName.data
            username = form.userName.data
            email = form.email.data
            gender = form.gender.data
            password = form.password.data
            category = form.category.data
            phone = form.phone.data
            user = User.query.get(email)
            if user is None:
                user = User(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    phone=phone,
                    email=email,
                    gender=gender,
                    role=Role.query.get(2),
                    category=Category.query.get(category)
                )
                user.make_password(password)
                user.save()
                login_user(user, remember=True)
                # TODO: review the reservation/account flow
                status_code, response = send_confirmation(user.email, user.full_name)
                if status_code == 200:
                    flash("A confirmation email has been sent via email.", "success")
                    return redirect(url_for("main.main_page"))
                else:
                    e = "An error occurred: Failed to send confirmation email."
                    current_app.logger.error(e)
                    flash("An internal server error happened.", "danger")
                    # return render_template('partials/500.html', error=e), 500
                    return redirect(url_for("main.main_page"))
            else:
                # TODO: there's a logic error here, fix it!
                errors = f"hey, There's a user with this email: {email}"
                return render_template("auth/signup.html", form=form, errors=errors)
        errors = f"Please check your form data again"
        return render_template("auth/signup.html", form=form, errors=errors)
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
@login_required
def confirm_email(token):
    if current_user.activated:
        flash("Account already confirmed.", "success")
        return redirect(url_for("main.main_page"))
    email = confirm_token(token)
    user = User.query.filter_by(email=current_user.email).first_or_404()
    if user.email == email:
        user.activated = True
        db.session.add(user)
        db.session.commit()
        flash("You have confirmed your account. Thanks!", "success")
    else:
        flash("The confirmation link is invalid or has expired.", "danger")
    return redirect(url_for('main.profile.profile'))

