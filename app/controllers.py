from flask import render_template, request, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from app import app, models, forms, login


# TODO: Remove this unused stuff
imgUrl = "https://via.placeholder.com/300/777777/FFFFFF/?text=Space"
spaces = [
        {"imgUrl": imgUrl, "title": "title1", "description": "des1"},
        {"imgUrl": imgUrl, "title": "title2", "description": "des2"},
        {"imgUrl": imgUrl, "title": "title3", "description": "des3"}
]

@app.route("/")
@login_required
def main_page():
    return render_template('default/home.html', spaces=spaces, name="hello")


@app.route("/signup", methods=["GET", "POST"])
def signup_page():
    form = forms.SignupForm()
    if request.method == "POST":
        if form.validate_on_submit():
            username = form.userName.data
            email = form.email.data
            password = form.password.data
            # TODO: get category input from user

            user = models.User.query.get(email)

            if user == None:
                # TODO: Edit the category with user input
                user = models.User(
                    username=username,
                    email=email,
                    role="user",
                    category="Internal"
                    )
                
                user.make_password(password)
                user.save()
            
            # TODO: there's a logic error here, fix it!
            errors = f"hey, There's a user with this email: {email}"
            # render_template does autoescaping html form input data
            return render_template("default/signup.html", form=form, errors=errors)
        errors = f"Please check your form data again"
        return render_template("default/signup.html", form=form, errors=errors)
    return render_template("default/signup.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for("main_page"))
    
    form = forms.LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # user = models.User.query.get()
        # filter users by username and then get first one
        user = models.User.query.filter_by(username=username).first()

        print(f"login username: {username}")
        print(f"login user object: {user}")

        if user is None and not user.verify_password(password):
                msg = "Invalid username or password."
                # render_template does autoescaping html form input data
                return render_template("login.html", form=form, msg=msg)
        
        # remember the user when he visits other pages
        # TODO: add remember me button to the form
        login_user(user, remember=True)
        return redirect(url_for("main_page"))
    return render_template("default/login.html", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main_page'))