from flask import (
    render_template, request, redirect,
    url_for
)
from flask_login import current_user, login_required

from app import db
from app.dashboard.tool import bp
from app.dashboard.tool.forms import ToolForm
from app.models import Space, Tool, Image, Category
from app.utils import save_file


@bp.route('/', methods=["GET", "POST"])
@login_required
def tool_list():
    if current_user.role.name == "admin":
        data = Tool.query.all()
        return render_template('dashboard/tool/index.html', tools=data)


@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete_tool(id):
    if current_user.role.name == "admin":
        tool = Tool.query.get(id)
        images = Image.query.filter_by(tool_id=id)
        for image in images:
            db.session.delete(image)
        for cat_price in tool.category_prices:
            db.session.delete(cat_price)
        db.session.delete(tool)
        db.session.commit()
        return redirect(url_for("dashboard.tool.tool_list"))
    else:
        return redirect(url_for("main.main_page"))


@bp.route("/create", methods=["GET", "POST"])
@login_required
def create_tool():
    spaces = Space.query.all()
    form = ToolForm()
    categories = Category.query.all()
    form.space.choices = [(s.id, s.name) for s in spaces]
    form.space.choices.insert(0, (0, "-- اختر المساحة --"))
    if current_user.role.name == "admin":
        space_selected = form.space.data and not form.space.data == '0'
        cp_tmp = list(form.category_prices.data)
        has_deleted_entries = any([True for cp in cp_tmp if cp['delete']])
        if has_deleted_entries:
            form.category_prices.process(None)
            for cp in cp_tmp:
                if cp['delete']:
                    continue
                form.category_prices.append_entry(cp)
        if (
                form.validate_on_submit() and
                not form.add_new_price.data and
                not has_deleted_entries
        ):
            tool = Tool(
                name=form.name.data,
                has_operator=form.has_operator.data,
                description=form.description.data,
                guidelines=form.guidelines.data,
                quantity=form.quantity.data,
                space=Space.query.get(
                    form.space.data) if space_selected else None
            )
            tool.set_category_prices(
                form.category_prices.data, categories, space_selected
            )
            images_objs = list()
            for file in form.images.data:
                if not file:
                    continue
                url = save_file("tool", file)
                images_objs.append(Image(tool=tool, url=url))
            tool.images = images_objs
            db.session.add(tool)
            db.session.commit()
            return redirect(url_for("dashboard.tool.tool_list"))
        cat_prices = [
            {"category_id": cat.id}
            for cat in categories
        ]
        if not space_selected and not has_deleted_entries:
            form.category_prices.append_entry({"price_list": cat_prices})
        return render_template("dashboard/tool/form.html", form=form, categories=categories)
    else:
        return redirect(url_for("main.main_page"))


@bp.route("/<int:id>/update", methods=["GET", "POST"])
@login_required
def update_tool(id):
    if current_user.role.name == "admin":
        spaces = Space.query.all()
        form = ToolForm()
        form.space.choices = [(s.id, s.name) for s in spaces]
        form.space.choices.insert(0, (0, "-- اختر المساحة --"))
        tool = Tool.query.get(id)
        categories = Category.query.all()

        cp_tmp = list(form.category_prices.data)
        has_deleted_entries = any([True for cp in cp_tmp if cp['delete']])
        if has_deleted_entries:
            form.category_prices.process(None)
            for cp in cp_tmp:
                if cp['delete']:
                    continue
                form.category_prices.append_entry(cp)

        if request.method == "GET":
            form.name.data = tool.name
            form.quantity.data = tool.quantity
            form.images.data = tool.images
            form.guidelines.data = tool.guidelines
            form.description.data = tool.description
            form.has_operator.data = tool.has_operator
            form.space.data = str(
                tool.space.id) if not tool.space == None else "0"

            form.process_cat_prices(tool.get_category_prices())
            return render_template(
                'dashboard/tool/form.html',
                form=form, isUpdate=True, tool=tool, categories=categories
            )
        elif request.method == "POST":
            space_selected = form.space.data and not form.space.data == '0'
            if (
                    form.validate_on_submit() and
                    not form.add_new_price.data and
                    not has_deleted_entries
            ):
                tool.name = form.name.data
                tool.has_operator = form.has_operator.data
                tool.description = form.description.data
                tool.guidelines = form.guidelines.data
                tool.quantity = form.quantity.data
                tool.space = Space.query.get(
                    form.space.data) if not form.space.data == 0 else None

                for cat_price in tool.category_prices:
                    db.session.delete(cat_price)
                db.session.commit()
                tool.set_category_prices(
                    form.category_prices.data, categories, space_selected
                )

                images_objs = list()
                for file in form.images.data:
                    print(file)
                    if not file:
                        continue
                    url = save_file("tool", file)
                    images_objs.append(Image(tool=tool, url=url))
                db.session.add_all(images_objs)
                db.session.commit()
                return redirect(url_for("dashboard.tool.tool_list"))
            if (
                    form.validate_on_submit() and form.add_new_price.data and
                    not has_deleted_entries and not space_selected
            ):
                cat_prices = [
                    {"category_id": cat.id}
                    for cat in categories
                ]
                form.category_prices.append_entry({"price_list": cat_prices})
            return render_template(
                "dashboard/tool/form.html",
                form=form, isUpdate=True, tool=tool, categories=categories
            )
    else:
        return redirect(url_for("main.main_page"))
