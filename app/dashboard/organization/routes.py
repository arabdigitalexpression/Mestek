from flask import (
    render_template, request, redirect,
    url_for
)
from flask_login import current_user, login_required

from app import db
from app.dashboard.forms import ConfirmForm
from app.dashboard.organization import bp
from app.dashboard.organization.forms import OrganizationForm
from app.models import Organization, Category
from app.utils import save_file, remove_file


@bp.route('/')
@login_required
def organization_list():
    data = Organization.query.all()
    form = ConfirmForm()
    if current_user.role.name == "admin":
        return render_template('dashboard/organization/index.html', current_user=current_user, form=form,
                               organizations=data)
    else:
        return render_template("dashboard/index.html")


@bp.route('/<string:name>')
@login_required
def get_organization(name):
    organization = Organization.query.filter_by(name=name).first_or_404()
    if current_user.role.name == "admin":
        return render_template('dashboard/organization/details.html', organization=organization)
    else:
        return render_template("dashboard/index.html")


@bp.route('/<string:name>/delete', methods=['POST'])
@login_required
def delete_organization(name):
    form = ConfirmForm()
    if form.validate_on_submit() and form.value.data == name:
        organization = Organization.query.filter_by(name=name).first_or_404()
        db.session.delete(organization)
        db.session.commit()
        return redirect(url_for("dashboard.organization.organization_list"))


@bp.route('/create', methods=["GET", "POST"])
@login_required
def create_organization():
    categories = Category.query.filter_by(is_organization=True)
    form = OrganizationForm()
    form.category.choices = [(c.id, c.name) for c in categories]
    form.category.choices.insert(0, (0, "-- اختر تصنيف --"))
    if request.method == "POST":
        if form.validate_on_submit():
            name = form.name.data
            description = form.description.data
            address = form.address.data
            website_url = form.website_url.data
            category = form.category.data
            phone = form.phone.data
            organization = Organization.query.get(name)
            if organization is None:
                organization = Organization(
                    name=name,
                    description=description,
                    website_url=website_url,
                    address=address,
                    phone=phone,
                    logo_url=save_file("organization", form.logo_url.data) if form.logo_url.data else None,
                    category=Category.query.get(category) if not category == 0 else None
                )
                db.session.add(organization)
                db.session.commit()
                return redirect(url_for("dashboard.organization.organization_list"))
            errors = f"هناك مؤسسة مسجلة باسم: {name}"
            # render_template does autoescaping html form input data
            return render_template("dashboard/organization/form.html", form=form, errors=errors)
        errors = f"من فضلك تأكد من صحة البيانات"
        return render_template("dashboard/organization/form.html", form=form, errors=errors)
    return render_template("dashboard/organization/form.html", form=form)


@bp.route('/<string:name>/update', methods=["GET", "POST"])
@login_required
def update_organization(name):
    if current_user.role.name == "admin":
        categories = Category.query.filter_by(is_organization=True)
        form = OrganizationForm()
        form.category.choices = [(c.id, c.name) for c in categories]
        form.category.choices.insert(0, (0, "-- اختر تصنيف --"))
        organization = Organization.query.filter_by(name=name).first_or_404()
        if request.method == "GET":
            form.name.data = organization.name
            form.description.data = organization.description
            form.address.data = organization.address
            form.phone.data = organization.phone
            form.website_url.data = organization.website_url
            form.logo_url.data = organization.logo_url
            form.category.data = str(
                organization.category.id) if organization.category is not None else "0"
            return render_template(
                'dashboard/organization/form.html',
                form=form, isUpdate=True, organization=organization
            )
        elif request.method == "POST":
            organization.name = form.name.data
            organization.description = form.description.data
            organization.address = form.address.data
            organization.phone = form.phone.data
            organization.website_url = form.website_url.data
            if organization.logo_url:
                remove_file("organization", organization.logo_url.split("/")[-1])
            if form.logo_url.data:
                organization.logo_url = save_file("organization", form.logo_url.data)
            organization.category = Category.query.get(
                form.category.data) if not form.category.data == 0 else None
            db.session.commit()
            return redirect(url_for("dashboard.organization.organization_list"))
    else:
        return redirect(url_for("main.main_page"))
