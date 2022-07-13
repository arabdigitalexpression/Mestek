import os
import re
from flask import (
    render_template, request, redirect,
    url_for, send_file
)
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.utils import secure_filename
from app import app, db, login
from app.models import (
    User, Space, Tool, Image
)
from app.forms import (
    SignupForm, LoginForm, SpaceForm, ToolForm
)


@app.route("/")
@login_required
def main_page():
    return render_template('default/home.html', name="hello")


@app.route("/signup", methods=["GET", "POST"])
def signup_page():
    form = SignupForm()
    if request.method == "POST":
        if form.validate_on_submit():
            username = form.userName.data
            email = form.email.data
            password = form.password.data
            # TODO: get category input from user

            user = User.query.get(email)

            if user == None:
                # TODO: Edit the category with user input
                user = User(
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

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # user = User.query.get()
        # filter users by username and then get first one
        user = User.query.filter_by(username=username).first()

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


@app.route('/dashboard/')
@login_required
def dashboard():        
    if current_user.role == "admin":
        return render_template("dashboard/index.html")
    else:
        return redirect(url_for('main_page'))


@app.route('/spaces')
def space_list():
    data = Space.query.all()
    if current_user.role == "admin":
        return render_template('dashboard/space/table.html', spaces=data)
    else:
        return render_template("spaces.html", spaces=data)


@app.route('/space/<int:id>/delete', methods=['POST'])
def delete_space(id):
    space = Space.query.get(id)
    db.session.delete(space)
    db.session.commit()
    return redirect(url_for("space_list"))


@app.route("/space/create", methods=["GET", "POST"])
@login_required
def create_space():
    form = SpaceForm()
    if current_user.role == "admin":
        if form.validate_on_submit():
            space = Space(
                name = form.name.data,
                price = form.price.data,
                has_operator = form.has_operator.data,
                description = form.description.data,
                guidelines = form.guidelines.data
            )
            imagesObjs = list()
            # print(dir(form.images.data[0]))
            for file in form.images.data:
                if file.content_length == 0:
                    continue
                filename = secure_filename(file.filename)
                # TODO: image is overwritten when there's 
                # an existing image with the same name
                file.save(os.path.join(
                    app.config["APP_PATH"],
                    app.config["UPLOAD_PATH"],
                    "space",
                    filename
                ))
                imagesObjs.append(Image(
                    url = url_for(
                        "download_file",
                        dir="space",
                        filename=filename
                        )
                ))
            space.images = imagesObjs
            db.session.add(space)
            db.session.commit()
            return redirect(url_for("space_list"))
        return render_template("dashboard/space/form.html", form=form)
    else:
        return redirect(url_for("main_page"))


@app.route("/space/<int:id>/update", methods=["GET", "POST"])
@login_required
def update_space(id):
    if current_user.role == "admin":
        form = SpaceForm()
        space = Space.query.get(id)
        if request.method == "GET":
            form.name.data = space.name
            form.price.data = space.price
            form.images.data = space.images
            form.guidelines.data = space.guidelines
            form.description.data = space.description
            form.has_operator.data = space.has_operator
            return render_template(
                'dashboard/space/form.html',
                form=form, isUpdate=True, space=space
            )
        elif request.method == "POST":
            if form.validate_on_submit():
                space.name = form.name.data
                space.price = form.price.data
                space.has_operator = form.has_operator.data
                space.description = form.description.data
                space.guidelines = form.guidelines.data
                imagesObjs = list()
                for file in form.images.data:
                    if file.content_length == 0:
                        continue
                    filename = secure_filename(file.filename)
                    # TODO: image is overwritten when there's 
                    # an existing image with the same name
                    file.save(os.path.join(
                        app.config["APP_PATH"],
                        app.config["UPLOAD_PATH"],
                        "space",
                        filename
                    ))
                    imagesObjs.append(Image(
                        space=space,
                        url = url_for(
                        "download_file",
                        dir="space",
                        filename=filename
                        )
                    ))
                db.session.add_all(imagesObjs)
                db.session.commit()
                return redirect(url_for("space_list"))
            return render_template(
                "dashboard/space/form.html",
                form=form, isUpdate=True, space=space
            )
    else:
        return redirect(url_for("main_page"))


# Tools
@app.route('/tools')
def tool_list():
    data = Tool.query.all()
    if current_user.role == "admin":
        return render_template('dashboard/tool/table.html', tools=data)
    else:
        return render_template("tools.html", tools=data)


@app.route('/tool/<int:id>/delete', methods=['POST'])
def delete_tool(id):
    tool = Tool.query.get(id)
    db.session.delete(tool)
    db.session.commit()
    return redirect(url_for("tool_list"))


@app.route("/tool/create", methods=["GET", "POST"])
@login_required
def create_tool():
    spaces = Space.query.all()
    form = ToolForm()
    form.space.choices = [(s.id, s.name) for s in spaces]
    if current_user.role == "admin":
        if form.validate_on_submit():
            tool = Tool(
                name = form.name.data,
                price = form.price.data,
                has_operator = form.has_operator.data,
                description = form.description.data,
                guidelines = form.guidelines.data,
                space = Space.query.get(form.space.data)
            )
            imagesObjs = list()
            for file in form.images.data:
                if file.content_length == 0:
                    continue
                filename = secure_filename(file.filename)
                # TODO: image is overwritten when there's 
                # an existing image with the same name
                file.save(os.path.join(
                    app.config["APP_PATH"],
                    app.config["UPLOAD_PATH"],
                    "tool",
                    filename
                ))
                imagesObjs.append(Image(
                    url = url_for(
                        "download_file",
                        dir="tool",
                        filename=filename
                        )
                ))
            tool.images = imagesObjs
            db.session.add(tool)
            db.session.commit()
            return redirect(url_for("tool_list"))
        return render_template("dashboard/tool/form.html", form=form)
    else:
        return redirect(url_for("main_page"))


@app.route("/tool/<int:id>/update", methods=["GET", "POST"])
@login_required
def update_tool(id):
    if current_user.role == "admin":
        spaces = Space.query.all()
        form = ToolForm()
        form.space.choices = [(s.id, s.name) for s in spaces]
        tool = Tool.query.get(id)
        if request.method == "GET":
            form.name.data = tool.name
            form.price.data = tool.price
            form.images.data = tool.images
            form.guidelines.data = tool.guidelines
            form.description.data = tool.description
            form.has_operator.data = tool.has_operator
            return render_template(
                'dashboard/tool/form.html',
                form=form, isUpdate=True, tool=tool
            )
        elif request.method == "POST":
            if form.validate_on_submit():
                tool.name = form.name.data
                tool.price = form.price.data
                tool.has_operator = form.has_operator.data
                tool.description = form.description.data
                tool.guidelines = form.guidelines.data
                tool.space = Space.query.get(form.space.data)
                imagesObjs = list()
                for file in form.images.data:
                    if file.content_length == 0:
                        continue
                    filename = secure_filename(file.filename)
                    # TODO: image is overwritten when there's 
                    # an existing image with the same name
                    file.save(os.path.join(
                        app.config["APP_PATH"],
                        app.config["UPLOAD_PATH"],
                        "tool",
                        filename
                    ))
                    imagesObjs.append(Image(
                        tool=tool,
                        url = url_for(
                        "download_file",
                        dir="tool",
                        filename=filename
                        )
                    ))
                db.session.add_all(imagesObjs)
                db.session.commit()
                return redirect(url_for("tool_list"))
            return render_template(
                "dashboard/tool/form.html",
                form=form, isUpdate=True, tool=tool
            )
    else:
        return redirect(url_for("main_page"))


@app.route('/uploads/<dir>/<filename>')
def download_file(dir, filename):
    return send_file(os.path.join(
        app.config["APP_PATH"],
        app.config["UPLOAD_PATH"],
        f'{dir}/{filename}'
    ))