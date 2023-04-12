import datetime
import math
from flask_wtf import FlaskForm

from flask import (
    render_template, redirect, url_for, request,
)
from flask_login import current_user, login_required

from app import db
from app.dashboard.reservation import bp
from app.dashboard.reservation.forms import ReservationUpdateForm
from app.enums import PaymentTypes
from app.models import (
    Reservation, Space, Tool, User,
    Calendar, Interval
)


@bp.route('/', methods=["GET", "POST"])
@login_required
def get_reservations():
    i = 1
    j = 10
    if current_user.role.name == "admin":
        reservations = Reservation.query.all()
        rows = int(Reservation.query.count())

        if rows == 0:
            pages = 0
        elif rows % 10 == 0:
            pages = rows / 10
        else:
            pages = math.trunc(rows / 10) + 1

        if request.method == 'POST':
            if request.form.get("b") != None:
                num = int(request.form.get("b"))
                global x
                x = int(request.form.get("b"))
                i = int(str(num - 1) + "1")
                j = int(str(num) + "0")
            elif request.form.get("next") == "next":
                try:
                    x
                except NameError:
                    x = 1
                x += 1
                if x >= pages:
                    x = pages
                i = int(str(x - 1) + "1")
                j = int(str(x) + "0")

            elif request.form.get("Previous") == "Previous":
                try:
                    x
                except NameError:
                    x = 1
                x -= 1
                if x <= 0:
                    x = 1
                i = int(str(x - 1) + "1")
                j = int(str(x) + "0")

        return render_template(
            "dashboard/reservation/index.html",
            reservations=reservations, i=i, j=j, pages=int(pages))
    return redirect(url_for("main.main_page"))


@bp.route('/<int:pk>/', methods=["GET", "POST"])
@login_required
def update_reservation(pk):
    if current_user.role.name == "admin":
        form = ReservationUpdateForm(request.form)
        reservation = Reservation.query.get_or_404(pk)
        form.payment_status.choices = PaymentTypes.choices()
        if request.method == "GET":
            form.transaction_num.data = reservation.transaction_num
            form.payment_status.data = str(reservation.payment_status.name)
            form.discount.data = reservation.discount
            return render_template(
                'dashboard/reservation/details.html',
                form=form, reservation=reservation
            )
        elif request.method == "POST":
            if form.validate_on_submit():
                form.populate_obj(reservation)
                db.session.commit()
                return redirect(url_for("dashboard.reservation.get_reservations"))
            return render_template(
                'dashboard/reservation/details.html',
                form=form, reservation=reservation
            )
    return redirect(url_for('main.main_page'))


@bp.route('/create/space/', methods=["GET", "POST"])
@login_required
def create_reservation_space():
    form = FlaskForm()
    reserve = Space.query.all()
    tool = Tool.query.all()
    users = User.query.all()
    if current_user.role.name == "admin":
        if request.method == "POST":
            if request.form.get("confirm") == "confirm":
                if request.form.get("username") == "noAccount":
                    user_id = current_user.get_id()
                else:
                    user_id = request.form.get("username")
                payment_status = request.form.get("payment")
                name = request.form.get("spaceName")
                val = name.split('&')
                full_price = val[1]

                space = Reservation(
                    space_id=val[0],
                    type="space",
                    payment_status=payment_status,
                    user_id=user_id,
                    full_price=full_price
                )
                db.session.add(space)
                start_date_range = request.form.get("start_date_range")
                end_date_range = request.form.get("end_date_range")
                date_no_range = request.form.get("date_from_to_no_range")
                ########## Save Range_date ###########################

                if start_date_range and end_date_range != "":

                    start_date = start_date_range.split("/")
                    end_date = end_date_range.split("/")
                    days = int(start_date[2])
                    counter = int(end_date[2]) - int(start_date[2])
                    if start_date[0] == end_date[0] and start_date[1] == end_date[1]:
                        if request.form.get("check-sa") == "on" and request.form.get("check-fr") == "on":
                            for count in range(counter + 1):
                                ans = datetime.date(
                                    int(start_date[0]), int(start_date[1]), int(days))
                                final_date = start_date[0] + "-" + \
                                    start_date[1] + "-" + str(days)
                                Dates = Calendar(
                                    day=final_date
                                )
                                Dates.reservations.append(space)
                                ##############################################################
                                db.session.add(Dates)
                                days += 1

                        elif request.form.get("check-sa") == None and request.form.get("check-fr") == "on":
                            for count in range(counter + 1):
                                ans = datetime.date(
                                    int(start_date[0]), int(start_date[1]), int(days))
                                print(request.form.get("check-sa"))
                                if ans.strftime("%A") != "Saturday":
                                    final_date = start_date[0] + "-" + \
                                        start_date[1] + "-" + str(days)
                                    Dates = Calendar(
                                        day=final_date
                                    )
                                    Dates.reservations.append(space)
                                    ##############################################################
                                    db.session.add(Dates)
                                days += 1

                        elif request.form.get("check-sa") == "on" and request.form.get("check-fr") == None:
                            for count in range(counter + 1):
                                ans = datetime.date(
                                    int(start_date[0]), int(start_date[1]), int(days))
                                print(request.form.get("check-sa"))
                                if ans.strftime("%A") != "Friday":
                                    final_date = start_date[0] + "-" + \
                                        start_date[1] + "-" + str(days)
                                    Dates = Calendar(
                                        day=final_date
                                    )
                                    Dates.reservations.append(space)
                                    ##############################################################
                                    db.session.add(Dates)
                                days += 1

                        elif request.form.get("check-sa") == None and request.form.get("check-fr") == None:
                            for count in range(counter + 1):
                                ans = datetime.date(
                                    int(start_date[0]), int(start_date[1]), int(days))
                                print(request.form.get("check-sa"))
                                if ans.strftime("%A") != "Saturday" and ans.strftime("%A") != "Friday":
                                    final_date = start_date[0] + "-" + \
                                        start_date[1] + "-" + str(days)
                                    Dates = Calendar(
                                        day=final_date
                                    )
                                    Dates.reservations.append(space)
                                ##############################################################
                                db.session.add(Dates)
                                days += 1
                ########## Save no_ Range_date ###########################
                elif date_no_range != "":

                    dates = date_no_range.split(",")

                    for final_date in dates:
                        time1 = request.form.get("time_picker_no_range")
                        time2 = request.form.get("time2_picker_no_range")
                        ftime = time1.split(" ")
                        etime = time2.split(" ")
                        Time1 = ftime[0]
                        Time2 = etime[0]
                        finaltime = Interval(
                            start_time=str(Time1) + ":00",
                            end_time=str(Time2) + ":00",
                        )
                        Dates = Calendar(
                            day=final_date
                        )
                        # 1st way
                        finaltime.calendar = Dates
                        finaltime.reservation = space
                        db.session.add(finaltime)

                        db.session.add(Dates)
                        # 2nd way
                        # Dates.intervals.append(finaltime)
                    db.session.commit()

                return redirect(url_for("get_reservations"))
            if request.form.get("chooseTool") == "chooseTool":
                if request.form.get("spaceName") == 'hide':
                    return render_template('dashboard/reservation/form/space.html', reserve1=reserve, tools=tool)
                else:
                    name = request.form.get("spaceName")
                    val1 = name.split('&')

                    datetime1 = request.form.get('datetimes')
                    return render_template('dashboard/reservation/form/adminSpaceWithTool.html', id=int(val1[0]),
                                           reserve1=reserve, tools=tool, name=val1[2], datetime=datetime1,
                                           price=val1[1], users=users)

            if request.form.get("confirmWithTool") == "confirmWithTool":
                name = request.form.get("toolName")
                val = name.split('&')
                if request.form.get("username") == "noAccount":
                    user_id = current_user.get_id()
                else:
                    user_id = request.form.get("username")
                payment_status = request.form.get("payment")
                space = Reservation(
                    # reservation for Space
                    space_id=val[0],
                    type="space",
                    payment_status=payment_status,
                    user_id=user_id,
                    full_price=val[1],
                )
                db.session.add(space)

                tools = Reservation(
                    tool_id=val[2],
                    type="tool",
                    payment_status=payment_status,
                    user_id=user_id,
                    full_price=val[3]
                )
                db.session.add(tools)
                start_date_range = request.form.get("start_date_range")
                end_date_range = request.form.get("end_date_range")
                date_no_range = request.form.get("date_from_to_no_range")
                ########## Save Range_date ###########################

                if start_date_range and end_date_range != "":

                    start_date = start_date_range.split("/")
                    end_date = end_date_range.split("/")
                    days = int(start_date[2])
                    counter = int(end_date[2]) - int(start_date[2])
                    if start_date[0] == end_date[0] and start_date[1] == end_date[1]:
                        for count in range(counter + 1):
                            ans = datetime.date(
                                int(start_date[0]), int(start_date[1]), int(days))
                            print(ans.strftime("%A"))
                            if ans.strftime("%A") != "Saturday" and ans.strftime("%A") != "Friday":
                                final_date = start_date[0] + "-" + \
                                    start_date[1] + "-" + str(days)
                                Dates = Calendar(
                                    day=final_date
                                )
                                Dates.reservations.append(space)
                                ##############################################################
                                db.session.add(Dates)
                            days += 1
                ########## Save no_ Range_date ###########################
                elif date_no_range != "":
                    dates = date_no_range.split(",")

                    for final_date in dates:
                        Dates = Calendar(
                            day=final_date
                        )
                        Dates.reservations.append(space)
                        db.session.add(Dates)

                    time1 = request.form.get("time_picker_no_range")
                    time2 = request.form.get("time2_picker_no_range")
                    ftime = time1.split(" ")
                    etime = time2.split(" ")
                    Time1 = int(ftime[0])
                    Time2 = int(etime[0])

                    finaltime = Interval(
                        start_time=str(Time1) + ":00:00",
                        end_time=str(Time2) + ":00:00",
                    )
                    db.session.add(finaltime)

                db.session.commit()
                return redirect(url_for("get_reservations"))
            if request.form.get("cancel") == "cancel":
                return redirect(url_for('main.main_page'))
        return render_template('dashboard/reservation/form/space.html', reserve1=reserve, tools=tool,
                               users=users, form=form)


@bp.route('/create/tool/', methods=["GET", "POST"])
@login_required
def create_reservation_tool():
    tool = Tool.query.all()
    users = User.query.all()
    form = FlaskForm()
    if current_user.role.name == "admin":
        if request.method == 'POST':
            if request.form.get("username") == "noAccount":
                user_id = current_user.get_id()
            else:
                user_id = request.form.get("username")

            payment_status = request.form.get("payment")
            value = request.form.get("toolName")
            val = value.split('&')
            tool_id = val[0]
            full_price = val[1]

            tools = Reservation(
                tool_id=tool_id,
                type="tool",
                payment_status=payment_status,
                user_id=user_id,
                full_price=full_price
            )

            start_date_range = request.form.get("start_date_range")
            end_date_range = request.form.get("end_date_range")

            if start_date_range and end_date_range != "":

                start_date = start_date_range.split("/")
                end_date = end_date_range.split("/")
                days = int(start_date[2])
                counter = int(end_date[2]) - int(start_date[2])
                if start_date[0] == end_date[0] and start_date[1] == end_date[1]:
                    for count in range(counter + 1):
                        ans = datetime.date(
                            int(start_date[0]), int(start_date[1]), int(days))
                        print(ans.strftime("%A"))
                        if ans.strftime("%A") != "Saturday" and ans.strftime("%A") != "Friday":
                            final_date = start_date[0] + "-" + \
                                start_date[1] + "-" + str(days)
                            Dates = Calendar(
                                day=final_date
                            )
                            Dates.reservations.append(tools)
                            ##############################################################
                            db.session.add(Dates)
                        days += 1

            db.session.add(tools)
            db.session.commit()
            return redirect(url_for("get_reservations"))
        return render_template('dashboard/reservation/form/tool.html', tools=tool, users=users, form=form)


@bp.route('/<int:id>/delete', methods=["POST"])
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
        return redirect(url_for("dashboard.reservation.get_reservations"))
    return redirect(url_for("main.main_page"))


@bp.route('/<int:id>/change-payment-status')
def change_payment_status(id):
    pass
