from flask import render_template, request

from app import app, models, forms
# from app.forms import SignupForm, LoginForm


imgUrl = "https://via.placeholder.com/300/777777/FFFFFF/?text=Space"
spaces = [
        {"imgUrl": imgUrl, "title": "title1", "description": "des1"},
        {"imgUrl": imgUrl, "title": "title2", "description": "des2"},
        {"imgUrl": imgUrl, "title": "title3", "description": "des3"}
]

@app.route("/")
def main_page():
    return render_template('home.html', spaces=spaces, name="hello")


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
            
            errors = f"hey, There's a user with this email: {email}"
            # render_template does autoescaping html form input data
            return render_template("signup.html", form=form, errors=errors)
        errors = f"Please check your form data again"
        return render_template("signup.html", form=form, errors=errors)
    return render_template("signup.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login_page():
    form = forms.LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data

            # user = models.User.query.get()
            user = models.User.query.filter_by(username=username).first()

            print(f"login username: {username}")
            print(f"login user object: {user}")

            if user:
                if user.verify_password(password):
                    msg = f"hey, my dude, your username is {user.username}"
                    # render_template does autoescaping html form input data
                    return render_template("login.html", form=form, msg=msg)

            msg = f"who are you?"
            # render_template does autoescaping html form input data
            return render_template("login.html", form=form, msg=msg)
        return render_template("login.html", form=form)
    return render_template("login.html", form=form)