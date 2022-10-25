import os
from jinja2 import Undefined
import pymysql
connection = pymysql.connect(host='localhost',user='root',password='',database='srs',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
import math
from flask import (
    render_template, request, redirect,
    url_for, send_file
)
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.utils import secure_filename
from app import app, db, login
from app.models import (
    Category, Reservation, Role,
    User, Space, Tool, Image, Calendar, Interval
)
from app.forms import (
    ConfirmForm, RoleCategoryForm, SignupForm, LoginForm, SpaceForm, ToolForm
)
import datetime

@app.route("/")
@login_required
def main_page():
    return render_template('default/home.html', name="hello")


@app.route("/signup", methods=["GET", "POST"])
def signup_page():
    if current_user.is_authenticated:
        return redirect(url_for("main_page"))
    form = SignupForm()
    categories = Category.query.all()
    roles = Role.query.all()
    form.category.choices = [(c.id, c.name) for c in categories]
    form.category.choices.insert(0, ("", "-- اختر تصنيف --"))
    form.role.choices = [(r.id, r.name) for r in roles]
    if request.method == "POST":
        if form.validate_on_submit():
            first_name = form.firstName.data
            last_name = form.lastName.data
            username = form.userName.data
            email = form.email.data
            password = form.password.data
            category = form.category.data
            role = form.role.data
            user = User.query.get(email)
            if user == None:
                user = User(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    email=email,
                    role=Role.query.get(1),
                    category=Category.query.get(category)
                )
                user.make_password(password)
                user.save()
                login_user(user, remember=True)
                return redirect(url_for("main_page"))
            else:
                # TODO: there's a logic error here, fix it!
                errors = f"hey, There's a user with this email: {email}"
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
    if current_user.role.name == "admin":
        return render_template("dashboard/index.html")
    else:
        return redirect(url_for('main_page'))


@app.route('/dashboard/spaces'  , methods=["GET", "POST"])
@login_required
def space_list():
    i=1 
    j=10
    if current_user.role.name == "admin":
        data = Space.query.all()
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM space")
        data3 = cursor.fetchone()
        rows = data3['COUNT(*)']
        if rows%10==0:pages = rows/10
        else: pages = math.trunc(rows/10)+1

        if request.method == 'POST':
            if request.form.get("b") != None: 
                num = int(request.form.get("b"))
                global x
                x = int(request.form.get("b")) 
                i = int(str(num-1) + "1")
                j = int(str(num) + "0") 
            elif request.form.get("next") == "next":
                try:x
                except NameError:x=1
                x+=1
                print (pages)
                print (x)

                if x >= pages:x = pages
                i = int(str(x-1) + "1")
                j = int(str(x) + "0")  
                
            elif request.form.get("Previous") == "Previous":
                try:x
                except NameError:x=1
                x-=1
                if x <= 0:x = 1
                i = int(str(x-1) + "1")
                j = int(str(x) + "0")
        
        return render_template('dashboard/space/index.html', spaces=data , i=i , j=j  , pages=pages)
    


@app.route('/dashboard/space/<int:id>/delete', methods=['POST'])
@login_required
def delete_space(id):
    if current_user.role.name == "admin":
        space = Space.query.get(id)
        tools = Tool.query.filter_by(space_id=id)
        images = Image.query.filter_by(space_id=id)
        for tool in tools:
            tool.space_id = None
        for image in images:
            db.session.delete(image)   
        db.session.delete(space)
        db.session.commit()
        return redirect(url_for("space_list"))
    else:
        return redirect(url_for("main_page"))


@app.route("/dashboard/space/create", methods=["GET", "POST"])
@login_required
def create_space():
    form = SpaceForm()
    if current_user.role.name == "admin":
        if form.validate_on_submit():
            space = Space(
                name=form.name.data,
                price=form.price.data,
                has_operator=form.has_operator.data,
                description=form.description.data,
                guidelines=form.guidelines.data
            )
            imagesObjs = list()
            for file in form.images.data:
                if not file:
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
                    url=url_for(
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


@app.route("/dashboard/space/<int:id>/update", methods=["GET", "POST"])
@login_required
def update_space(id):
    if current_user.role.name == "admin":
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
                    if not file:
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
                        url=url_for(
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
@app.route('/dashboard/tools'  , methods=["GET", "POST"])
@login_required
def tool_list():
    i=1 
    j=10
    if current_user.role.name == "admin":
        data = Tool.query.all()
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM tool")
        data2 = cursor.fetchone()
        rows = data2['COUNT(*)']
        if rows%10==0:pages = rows/10
        else: pages = math.trunc(rows/10)+1
        if request.method == 'POST':
            if request.form.get("b") != None: 
                num = int(request.form.get("b"))
                global x
                x = int(request.form.get("b")) 
                i = int(str(num-1) + "1")
                j = int(str(num) + "0") 
            elif request.form.get("next") == "next":
                try:x
                except NameError:x=1
                x+=1
                print (pages)
                print (x)

                if x >= pages:x = pages
                i = int(str(x-1) + "1")
                j = int(str(x) + "0")  
                
            elif request.form.get("Previous") == "Previous":
                try:x
                except NameError:x=1
                x-=1
                if x <= 0:x = 1
                i = int(str(x-1) + "1")
                j = int(str(x) + "0")
        return render_template('dashboard/tool/index.html', tools=data , i=i , j=j  , pages=pages)
    


@app.route('/dashboard/tool/<int:id>/delete', methods=['POST'])
@login_required
def delete_tool(id):
    if current_user.role.name == "admin":
        tool = Tool.query.get(id)
        images = Image.query.filter_by(tool_id=id)
        for image in images:
            db.session.delete(image)
        db.session.delete(tool)
        db.session.commit()
        return redirect(url_for("tool_list"))
    else:
        return redirect(url_for("main_page"))


@app.route("/dashboard/tool/create", methods=["GET", "POST"])
@login_required
def create_tool():
    spaces = Space.query.all()
    form = ToolForm()
    form.space.choices = [(s.id, s.name) for s in spaces]
    form.space.choices.insert(0, (0, "-- اختر المساحة --"))
    if current_user.role.name == "admin":
        if form.validate_on_submit():
            tool = Tool(
                name=form.name.data,
                price=form.price.data,
                has_operator=form.has_operator.data,
                description=form.description.data,
                guidelines=form.guidelines.data,
                space=Space.query.get(
                    form.space.data) if not form.space.data == 0 else None
            )
            imagesObjs = list()
            for file in form.images.data:
                if not file:
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
                    url=url_for(
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


@app.route("/dashboard/tool/<int:id>/update", methods=["GET", "POST"])
@login_required
def update_tool(id):
    if current_user.role.name == "admin":
        spaces = Space.query.all()
        form = ToolForm()
        form.space.choices = [(s.id, s.name) for s in spaces]
        form.space.choices.insert(0, (0, "-- اختر المساحة --"))
        tool = Tool.query.get(id)
        if request.method == "GET":
            form.name.data = tool.name
            form.price.data = tool.price
            form.images.data = tool.images
            form.guidelines.data = tool.guidelines
            form.description.data = tool.description
            form.has_operator.data = tool.has_operator
            print(tool.space)
            form.space.data = str(tool.space.id) if not tool.space == None else "0" 
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
                tool.space = Space.query.get(
                    form.space.data) if not form.space.data == 0 else None
                imagesObjs = list()
                for file in form.images.data:
                    if not file:
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
                        url=url_for(
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


@app.route('/dashboard/users')
@login_required
def user_list():
    data = User.query.all()
    form = ConfirmForm()
    if current_user.role.name == "admin":
        return render_template('dashboard/user/index.html', current_user=current_user, form=form, users=data)
    else:
        return render_template("dashboard/index.html")


@app.route('/dashboard/user/<string:username>')
@login_required
def get_user(username):
    user = User.query.filter_by(username=username).first_or_404()
    if current_user.role.name == "admin":
        return render_template('dashboard/user/profile.html', user=user)
    else:
        return render_template("dashboard/index.html")


@app.route('/dashboard/user/<string:username>/delete', methods=['POST'])
@login_required
def delete_user(username):
    form = ConfirmForm()
    if form.validate_on_submit() and form.value.data == username:
        user = User.query.filter_by(username=username).first_or_404()
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for("user_list"))


@app.route("/dashboard/user/create", methods=["GET", "POST"])
@login_required
def create_user():
    categories = Category.query.all()
    roles = Role.query.all()
    form = SignupForm()
    form.category.choices = [(c.id, c.name) for c in categories]
    form.category.choices.insert(0, (0, "-- اختر تصنيف --"))
    form.role.choices = [(r.id, r.name) for r in roles]
    form.role.choices.insert(0,(0,"-- اختر صلاحية --")) 
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

            if user == None:
                user = User(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    email=email,
                    role=Role.query.get(role) if not role == 0 else None,
                    category=Category.query.get(category) if not category == 0 else None
                )

                user.make_password(password)
                user.save()
                return redirect(url_for("user_list"))
            # TODO: there's a logic error here, fix it!
            errors = f"hey, There's a user with this email: {email}"
            # render_template does autoescaping html form input data
            return render_template("dashboard/user/form.html", form=form, errors=errors)
        errors = f"Please check your form data again"
        return render_template("dashboard/user/form.html", form=form, errors=errors)
    return render_template("dashboard/user/form.html", form=form)


@app.route("/dashboard/user/<string:username>/update", methods=["GET", "POST"])
@login_required
def update_user(username):
    if current_user.role.name == "admin":
        categories = Category.query.all()
        roles = Role.query.all()
        form = SignupForm()
        form.category.choices = [(c.id, c.name) for c in categories]
        form.category.choices.insert(0, (0, "-- اختر تصنيف --"))
        form.role.choices = [(r.id, r.name) for r in roles]
        form.role.choices.insert(0,(0,"-- اختر صلاحية --")) 
        user = User.query.filter_by(username=username).first_or_404()
        if request.method == "GET":
            form.firstName.data = user.first_name
            form.lastName.data = user.last_name
            form.userName.data = user.username
            form.email.data = user.email
            form.role.data = str(user.role.id) if not user.role == None else "0"
            form.category.data = str(user.category.id) if not user.category == None else "0"
            return render_template(
                'dashboard/user/form.html',
                form=form, isUpdate=True, user=user
            )
        elif request.method == "POST":
            user.first_name = form.firstName.data
            user.last_name = form.lastName.data
            user.username = form.userName.data
            user.email = form.email.data
            user.role = Role.query.get(form.role.data) if not form.role.data == 0 else None
            user.category = Category.query.get(form.category.data) if not form.category.data == 0 else None
            user.make_password(form.password.data)
            db.session.commit()
            return redirect(url_for("user_list"))
    else:
        return redirect(url_for("main_page"))


@app.route("/dashboard/roles", methods=["GET", "POST"])
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
        return redirect(url_for("main_page"))


@app.route("/dashboard/categories", methods=["GET", "POST"])
@login_required
def get_categories():
    categories = Category.query.all()
    form = RoleCategoryForm()
    input = ConfirmForm()
    if current_user.role.name == "admin":
        if request.method == "POST":
            if form.validate_on_submit():
                name = form.name.data
                color_code = form.colorCode.data
                category = Category.query.get(name)
                if category == None:
                    category = Category(
                        name=name,
                        color_code=color_code,
                    )
                    db.session.add(category)
                    db.session.commit()
                    categories = Category.query.all()
                errors = f"hey, There's a category with this name: {name}"
                return render_template("dashboard/user/category/index.html", form=form, errors=errors, categories=categories, input=input)
            errors = f"Please check your form data again"
            return render_template("dashboard/user/category/index.html", form=form, errors=errors, categories=categories, input=input)
        return render_template("dashboard/user/category/index.html", form=form, categories=categories, input=input)
    else:
        return redirect(url_for("main_page"))


@app.route("/dashboard/role/<int:id>/update", methods=["GET", "POST"])
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
                return redirect(url_for("get_roles"))
            return render_template(
                "dashboard/user/role/index.html",
                form=form, isUpdate=True, roles=roles, input=input
            )
    else:
        return redirect(url_for("main_page"))


@app.route("/dashboard/category/<int:id>/update", methods=["GET", "POST"])
@login_required
def update_category(id):
    input = ConfirmForm()
    category = Category.query.get(id)
    if current_user.role.name == "admin":
        form = RoleCategoryForm()
        if request.method == "GET":
            categories = Category.query.all()
            form.name.data = category.name
            form.colorCode.data = category.color_code
            return render_template(
                'dashboard/user/category/index.html',
                form=form, isUpdate=True, categories=categories, category=category, input=input
            )
        elif request.method == "POST":
            categories = Category.query.all()
            if form.validate_on_submit():
                category.name = form.name.data
                category.color_code = form.colorCode.data
                db.session.commit()
                return redirect(url_for("get_categories"))
            return render_template(
                "dashboard/user/category/index.html",
                form=form, isUpdate=True, categories=categories, input=input
            )
    else:
        return redirect(url_for("main_page"))


@app.route('/dashboard/role/<int:id>/delete', methods=['POST'])
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
            return redirect(url_for("get_roles"))
    else:
        return redirect(url_for("main_page"))


@app.route('/dashboard/category/<int:id>/delete', methods=['POST'])
@login_required
def delete_category(id):
    if current_user.role.name == "admin":
        input = ConfirmForm()
        category = Category.query.get(id)
        if input.validate_on_submit() and input.value.data == category.name:
            users = User.query.filter_by(category_id=id).all()
            for user in users:
                db.session.delete(user)
            db.session.delete(category)
            db.session.commit()
            return redirect(url_for("get_categories"))
    else:
        return redirect(url_for("main_page"))


@app.route('/dashboard/reservations/' , methods=["GET", "POST"])
@login_required
def get_reservations():
    i=1 
    j=10
    if current_user.role.name == "admin":
        reservations = Reservation.query.all()
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM reservation")
        data = cursor.fetchone()
        rows = data['COUNT(*)']
        if rows%10==0:pages = rows/10
        else: pages = math.trunc(rows/10)+1
        print (pages)
         
        
        if request.method == 'POST':
            if request.form.get("b") != None: 
                num = int(request.form.get("b"))
                global x
                x = int(request.form.get("b")) 
                i = int(str(num-1) + "1")
                j = int(str(num) + "0") 
            elif request.form.get("next") == "next":
                try:x
                except NameError:x=1
                x+=1
                if x >= pages:x = pages
                i = int(str(x-1) + "1")
                j = int(str(x) + "0")  
                
            elif request.form.get("Previous") == "Previous":
                try:x
                except NameError:x=1
                x-=1
                if x <= 0:x = 1
                i = int(str(x-1) + "1")
                j = int(str(x) + "0")  
                
                
        return render_template(
            "dashboard/reservation/index.html",
            reservations=reservations , i=i , j=j  , pages=pages)
    return redirect(url_for("main_page"))


@app.route('/')
def change_payment_status():
    pass


@app.route('/dashboard/reservation/<int:id>/delete', methods=["POST"])
@login_required
def delete_reservation(id):
    if current_user.role.name == "admin":
        reservation = Reservation.query.get(id)
        # for cal in reservation.calendars:
        #     has_others = any(cal.query.filter(
        #         Calendar.reservations.any(
        #             Reservation.id!=reservation.id
        #     )))
        #     if not has_others:
        #         db.session.delete(cal)
        db.session.delete(reservation)
        db.session.commit()
        return redirect(url_for("get_reservations"))
    return redirect(url_for("main_page"))


@app.route ('/dashboard/reservation/create/space/' , methods=["GET", "POST"])
@login_required
def createReservation():
    reserve = Space.query.all()
    tool = Tool.query.all()
    users = User.query.all()
    if current_user.role.name == "admin":
        if request.method=="POST":
            if request.form.get("confirm") == "confirm":
                if request.form.get("username") =="noAccount":
                    user_id = current_user.get_id()
                else:
                    user_id = request.form.get("username")
                payment_status = request.form.get("payment")
                name = request.form.get("spaceName")
                val = name.split('&')
                full_price = val[1]
                
                space = Reservation(
                    space_id = val[0],
                    type = "space",
                    payment_status = payment_status,
                    user_id = user_id,
                    full_price = full_price
                )
                db.session.add(space)
                start_date_range = request.form.get("start_date_range")
                end_date_range = request.form.get("end_date_range")
                date_no_range = request.form.get("date_from_to_no_range")
                ########## Save Range_date ###########################
                
                if start_date_range and end_date_range != "": 
 
                    start_date = start_date_range.split("/")
                    end_date = end_date_range.split("/")
                    days = int (start_date[2])
                    counter = int(end_date[2]) - int(start_date[2])
                    if start_date[0] == end_date[0] and start_date[1] == end_date[1] :
                        if request.form.get ("check-sa") == "on" and request.form.get ("check-fr") == "on":
                            for count in range(counter+1):
                                ans = datetime.date(int(start_date[0]),int(start_date[1]), int(days))
                                final_date = start_date[0] + "-" + start_date[1] + "-" + str(days)
                                Dates = Calendar(
                                    day = final_date
                                )
                                Dates.reservations.append(space)
                                ##############################################################
                                db.session.add(Dates)
                                days += 1

                        elif request.form.get ("check-sa") == None and request.form.get ("check-fr") == "on":
                            for count in range(counter+1):
                                ans = datetime.date(int(start_date[0]),int(start_date[1]), int(days))
                                print( request.form.get ("check-sa"))
                                if ans.strftime("%A") != "Saturday":
                                    final_date = start_date[0] + "-" + start_date[1] + "-" + str(days)
                                    Dates = Calendar(
                                        day = final_date
                                    )
                                    Dates.reservations.append(space)
                                    ##############################################################
                                    db.session.add(Dates)
                                days += 1

                        elif request.form.get ("check-sa") == "on" and request.form.get ("check-fr") == None:
                            for count in range(counter+1):
                                ans = datetime.date(int(start_date[0]),int(start_date[1]), int(days))
                                print( request.form.get ("check-sa"))
                                if ans.strftime("%A") != "Friday":
                                    final_date = start_date[0] + "-" + start_date[1] + "-" + str(days)
                                    Dates = Calendar(
                                        day = final_date
                                    )
                                    Dates.reservations.append(space)
                                    ##############################################################
                                    db.session.add(Dates)
                                days += 1

                        elif request.form.get ("check-sa") == None and request.form.get ("check-fr") == None:
                            for count in range(counter+1):
                                ans = datetime.date(int(start_date[0]),int(start_date[1]), int(days))
                                print( request.form.get ("check-sa"))
                                if ans.strftime("%A") != "Saturday" and ans.strftime("%A") != "Friday":
                                    final_date = start_date[0] + "-" + start_date[1] + "-" + str(days)
                                    Dates = Calendar(
                                        day = final_date
                                    )
                                    Dates.reservations.append(space)
                                ##############################################################
                                db.session.add(Dates)
                                days += 1
                ########## Save no_ Range_date ###########################
                elif date_no_range !="" :
                    
                    dates = date_no_range.split(",")
                    
                    
                    for final_date in dates:
                        Dates = Calendar(
                            day = final_date
                        )
                        Dates.reservations.append(space)
                        db.session.add(Dates)
                        time1 = request.form.get ("time_picker_no_range")
                        time2 = request.form.get ("time2_picker_no_range")
                        ftime = time1.split(" ")
                        etime = time2.split(" ")
                        Time1 = int(ftime[0])
                        Time2 = int(etime[0])
                        finaltime = Interval (
                            start_time = str(Time1) +":00",
                            end_time = str(Time2) +":00",
                        )
                        db.session.add (finaltime)

                db.session.commit()
                return redirect(url_for("get_reservations"))
            if request.form.get("chooseTool") == "chooseTool":
                if request.form.get("spaceName") == 'hide':
                    return render_template('dashboard/reservation/createReservation/adminReserve.html' , reserve1=reserve , tools=tool )
                else:
                    name = request.form.get("spaceName")
                    val1 = name.split('&')
                    datetime1 = request.form.get('datetimes')
                    return render_template('dashboard/reservation/createReservation/adminSpaceWithTool.html', id=int(val1[0]) , reserve1=reserve , tools=tool , name=val1[2] , datetime=datetime1 ,price=val1[1] , users = users)
            if request.form.get("confirmWithTool") == "confirmWithTool":
                name = request.form.get("toolName")
                val = name.split('&')
                if request.form.get("username") =="noAccount":
                    user_id = current_user.get_id()
                else:
                    user_id = request.form.get("username")
                payment_status = request.form.get("payment")
                space = Reservation(
                    #reservation for Space
                    space_id = val[0],
                    type = "space",
                    payment_status = payment_status,
                    user_id = user_id,
                    full_price = val[1],   
                )
                db.session.add(space)
    
                tools = Reservation(
                    tool_id = val[2],
                    type = "tool",
                    payment_status = payment_status,
                    user_id = user_id,
                    full_price = val[3]
                )
                db.session.add(tools)
                start_date_range = request.form.get("start_date_range")
                end_date_range = request.form.get("end_date_range")
                date_no_range = request.form.get("date_from_to_no_range")
                ########## Save Range_date ###########################
                if start_date_range and end_date_range != "": 
 
                    start_date = start_date_range.split("/")
                    end_date = end_date_range.split("/")
                    days = int (start_date[2])
                    counter = int(end_date[2]) - int(start_date[2])
                    if start_date[0] == end_date[0] and start_date[1] == end_date[1] :
                        for count in range(counter+1):
                            ans = datetime.date(int(start_date[0]),int(start_date[1]), int(days))
                            print(ans.strftime("%A") )
                            if ans.strftime("%A") != "Saturday" and ans.strftime("%A") != "Friday":
                                final_date = start_date[0] + "-" + start_date[1] + "-" + str(days)
                                Dates = Calendar(
                                    day = final_date
                                )
                                Dates.reservations.append(space)
                                ##############################################################
                                db.session.add(Dates)
                            days += 1
                ########## Save no_ Range_date ###########################
                elif date_no_range !="" :
                    dates = date_no_range.split(",")
                    for final_date in dates:
                        Dates = Calendar(
                            day = final_date
                        )
                        Dates.reservations.append(space)
                        db.session.add(Dates)

                    time1 = request.form.get ("time_picker_no_range")
                    time2 = request.form.get ("time2_picker_no_range")
                    ftime = time1.split(" ")
                    etime = time2.split(" ")
                    Time1 = int(ftime[0])
                    Time2 = int(etime[0])
                    finaltime = Interval (
                        start_time = str(Time1) +":00:00",
                        end_time = str(Time2) +":00:00",
                    )
                    db.session.add (finaltime)
                    
                db.session.commit()
                return redirect(url_for("get_reservations"))
            if request.form.get("cancel") == "cancel":
                return redirect(url_for("main_page"))        
        return render_template('dashboard/reservation/createReservation/adminReserve.html' , reserve1=reserve , tools=tool , users = users)






@app.route ('/dashboard/reservation/create/tool/' , methods=["GET", "POST"] )
@login_required
def createReservationTool():
    tool = Tool.query.all()
    users = User.query.all()
    if current_user.role.name == "admin":
        if request.method == 'POST':
            if request.form.get("username") =="noAccount":
                user_id = current_user.get_id()
            else:
                user_id = request.form.get("username")
            
            payment_status = request.form.get("payment")
            value = request.form.get("toolName")
            val = value.split('&')
            tool_id = val[0]
            full_price = val[1]
            
            tools = Reservation(
                tool_id = tool_id,
                type = "tool",
                payment_status = payment_status,
                user_id = user_id,
                full_price = full_price
            )
            start_date_range = request.form.get("start_date_range")
            end_date_range = request.form.get("end_date_range")   
            
            if start_date_range and end_date_range != "": 
 
                start_date = start_date_range.split("/")
                end_date = end_date_range.split("/")
                days = int (start_date[2])
                counter = int(end_date[2]) - int(start_date[2])
                if start_date[0] == end_date[0] and start_date[1] == end_date[1] :
                    for count in range(counter+1):
                        ans = datetime.date(int(start_date[0]),int(start_date[1]), int(days))
                        print(ans.strftime("%A") )
                        if ans.strftime("%A") != "Saturday" and ans.strftime("%A") != "Friday":
                            final_date = start_date[0] + "-" + start_date[1] + "-" + str(days)
                            Dates = Calendar(
                                day = final_date
                            )
                            Dates.reservations.append(tools)
                            ##############################################################
                            db.session.add(Dates)
                        days += 1
            db.session.add(tools)
            db.session.commit()
            return redirect(url_for("get_reservations"))  
        return render_template('dashboard/reservation/createReservation/adminReserveTool.html',tools=tool , users =users)
    



@app.route ('/reservation/create/tool/' , methods=["GET", "POST"] )
@login_required
def userReservationTool():
    tool = Tool.query.all()
    res = Reservation()
    cal = Calendar()
    if current_user.role.name == "user":
        if request.method == 'POST':
            if request.form.get("confirm") == "confirm":
                value = request.form.get("toolName")
                val = value.split('&')
                user_id = current_user.get_id()
                tools = Reservation(
                    tool_id = val[0],
                    type = "tool",
                    payment_status = "no_payment",
                    user_id = user_id,
                    full_price = val[1]
                )
                db.session.add(tools)

                start_date_range = request.form.get("start_date_range")
                end_date_range = request.form.get("end_date_range")   
                
                if start_date_range and end_date_range != "": 
                
                    start_date = start_date_range.split("/")
                    end_date = end_date_range.split("/")
                    days = int (start_date[2])
                    counter = int(end_date[2]) - int(start_date[2])
                    if start_date[0] == end_date[0] and start_date[1] == end_date[1] :
                        for count in range(counter+1):
                            ans = datetime.date(int(start_date[0]),int(start_date[1]), int(days))
                            print(ans.strftime("%A") )
                            if ans.strftime("%A") != "Saturday" and ans.strftime("%A") != "Friday":
                                final_date = start_date[0] + "-" + start_date[1] + "-" + str(days)
                                Dates = Calendar(
                                    day = final_date
                                )
                                Dates.reservations.append(tools)
                                ##############################################################
                                db.session.add(Dates)
                            days += 1
                    # res.calendars.append(cal)
                    # db.session.add(res)
                db.session.commit()
                return redirect(url_for("main_page"))
            elif request.form.get("cancel") == "cancel":
                return redirect(url_for("main_page"))
        return render_template('/default/tool.html' ,tools=tool)


@app.route ('/reservation/create/space/' , methods=["GET", "POST"] )
@login_required
def userReservationSpace():
    reserve = Space.query.all()
    tool = Tool.query.all()
    if current_user.role.name == "user":
        if request.method == 'POST':
            if request.form.get("confirm") == "confirm":
                name = request.form.get("spaceName")
                val = name.split('&')
                user_id = current_user.get_id()
                space = Reservation(
                    space_id = val[0],
                    type = "space",
                    payment_status = "no_payment",
                    user_id = user_id,
                    full_price = val[1]
                    )
                db.session.add(space)

                start_date_range = request.form.get("start_date_range")
                end_date_range = request.form.get("end_date_range")
                date_no_range = request.form.get("date_from_to_no_range")
                ########## Save Range_date ###########################
                
                if start_date_range and end_date_range != "": 
 
                    start_date = start_date_range.split("/")
                    end_date = end_date_range.split("/")
                    days = int (start_date[2])
                    counter = int(end_date[2]) - int(start_date[2])
                    if start_date[0] == end_date[0] and start_date[1] == end_date[1] :
                        for count in range(counter+1):
                            ans = datetime.date(int(start_date[0]),int(start_date[1]), int(days))
                            print(ans.strftime("%A") )
                            if ans.strftime("%A") != "Saturday" and ans.strftime("%A") != "Friday":
                                final_date = start_date[0] + "-" + start_date[1] + "-" + str(days)
                                Dates = Calendar(
                                    day = final_date
                                )
                                ##############################################################
                                db.session.add(Dates)
                            days += 1
                        db.session.commit()
                    ########## Save no_ Range_date ###########################
                elif date_no_range !="" :
                    dates = date_no_range.split(", ")
                    for final_date in dates:
                        Dates = Calendar(
                            day = final_date
                        )
                        db.session.add(Dates)
                        time1 = request.form.get ("time_picker_no_range")
                        time2 = request.form.get ("time2_picker_no_range")  
                        ftime = time1.split(" ")
                        etime = time2.split(" ")
                        Time1 = ftime[0]
                        Time2 = etime[0]
                        finaltime = Interval (
                            start_time = str(Time1) +":00",
                            end_time = str(Time2) +":00",
                        )
                        db.session.add (finaltime)
                    db.session.commit()
                return redirect(url_for("main_page"))
            elif request.form.get("chooseTool") == "chooseTool":
                if request.form.get("spaceName") == 'hide': 
                    return render_template('default/space.html' , reserve1=reserve , tools=tool )
                else:
                    name = request.form.get("spaceName")
                    val1 = name.split('&')
                    datetime1 = request.form.get('datetimes')
                    return render_template('default/space_with_tool.html', id=int(val1[0]) , reserve1=reserve , tools=tool , name=val1[2] , datetime=datetime1 ,price=val1[1]) 
            elif request.form.get("confirmWithTool") == "confirmWithTool":
                name = request.form.get("toolName")
                val = name.split('&')
                user_id = current_user.get_id()
                space = Reservation(
                    #reservation for Space
                    space_id = val[0],
                    type = "space",
                    payment_status = "no_payment",
                    user_id = user_id,
                    full_price = val[1],   
                )
                db.session.add(space)
                db.session.commit()
                date_range = request.form.get("date_from_to")
                date_no_range = request.form.get("date_from_to_no_range")
                ########## Save Range_date ###########################
                if date_range != "":       
                    dates = date_range.split(",")
                    start_date = dates[0].split("/")
                    end_date = dates[1].split("/")
                    days = int (start_date[1])
                    counter = int(end_date[1]) - int(start_date[1])
                    if start_date[0] == end_date[0] and start_date[2] == end_date[2] :
                        for count in range(counter+1):
                            final_date = start_date[2] + "-" + start_date[0] + "-" + str(days)
                            days += 1
                            Dates = Calendar(
                                day = final_date
                            )
                                ##############################################################
                            db.session.add(Dates)
                        db.session.commit()
                    ########## Save no_ Range_date ###########################
                elif date_no_range !="" :
                    dates = date_no_range.split(", ")
                    for final_date in dates:
                        Dates = Calendar(
                            day = final_date
                        )
                        db.session.add(Dates)
                        time1 = request.form.get ("time_picker_no_range")
                        time2 = request.form.get ("time2_picker_no_range")  
                        ftime = time1.split(" ")
                        etime = time2.split(" ")
                        Time1 = int(ftime[0])
                        Time2 = int(etime[0])
                        if ftime[1] == "م":
                            Time1 += 12
                        if etime[1] == "م":
                            Time2 += 12
                        finaltime = Interval (
                            start_time = str(Time1) +":00:00",
                            end_time = str(Time2) +":00:00",
                        )
                        db.session.add (finaltime)

                    tools = Reservation(
                        tool_id = val[2],
                        type = "tool",
                        payment_status = "no_payment",
                        user_id = user_id,
                        full_price = val[3]
                    )
                    db.session.add(tools)
                    db.session.commit()
                    return redirect(url_for("main_page"))
            if request.form.get("cancel") == "cancel":
                return redirect(url_for("main_page"))
        return render_template('/default/space.html' , reserve1=reserve , tools=tool)


@app.route ('/guidelines/')
@login_required
def guidelines():
    return render_template('/default/guidelines.html')