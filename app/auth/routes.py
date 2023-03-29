from flask import (
    render_template, request, redirect,
    url_for
)
from flask_login import current_user, login_user, logout_user

from app.auth import bp
from app.auth.forms import SignupForm, LoginForm
from app.models import (
    Category, Role, User
)


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
