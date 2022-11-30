from flask import (
    render_template, redirect, url_for
)
from flask_login import current_user, login_required
from app.dashboard import bp


@bp.route('/')
@login_required
def dashboard():
    if current_user.role.name == "admin":
        return render_template("dashboard/index.html")
    else:
        return redirect(url_for('main.main_page'))


@bp.route('/calendar/')
@login_required
def get_calendar():
    if current_user.role.name == "admin":

        return render_template(
            "dashboard/reservation/calendar.html"
        )
    return redirect(url_for("main.main_page"))
