import datetime

from flask import (
    render_template, redirect, url_for, request,
)
from flask_login import current_user, login_required
from flask_wtf import FlaskForm

from app import db
from app.main.reservation import bp
from app.models import (
    Reservation, Space, Tool, Calendar, Interval
)


@bp.route('/create/tool/', methods=["GET", "POST"])
@login_required
def create_reservation_tool():
    tool = Tool.query.all()
    res = Reservation()
    cal = Calendar()
    form = FlaskForm()
    if current_user.role.name == "user":
        if request.method == 'POST':
            if request.form.get("confirm") == "confirm":
                value = request.form.get("toolName")
                val = value.split('&')
                user_id = current_user.get_id()
                tools = Reservation(
                    tool_id=val[0],
                    type="tool",
                    payment_status="no_payment",
                    user_id=user_id,
                    full_price=val[1]
                )
                db.session.add(tools)

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
                    # res.calendars.append(cal)
                    # db.session.add(res)
                db.session.commit()
                return redirect(url_for("main.main_page"))
            elif request.form.get("cancel") == "cancel":
                return redirect(url_for("main.main_page"))
        return render_template('/default/reservation/tool.html', tools=tool, form=form)
    elif current_user.role.name == "admin":
        return redirect(url_for("dashboard.reservation.create_reservation_tool"))


@bp.route('/create/space/', methods=["GET", "POST"])
@login_required
def create_reservation_space():
    reserve = Space.query.all()
    tool = Tool.query.all()
    form = FlaskForm()
    if current_user.role.name == "user":
        if request.method == 'POST':
            if request.form.get("confirm") == "confirm":
                name = request.form.get("spaceName")
                val = name.split('&')
                user_id = current_user.get_id()
                space = Reservation(
                    space_id=val[0],
                    type="space",
                    payment_status="no_payment",
                    user_id=user_id,
                    full_price=val[1]
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
                                ##############################################################
                                db.session.add(Dates)
                            days += 1

                        db.session.commit()
                    ########## Save no_ Range_date ###########################
                elif date_no_range != "":
                    dates = date_no_range.split(", ")
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
                        db.session.add(finaltime)
                        # raise Exception()
                        # 2nd way
                        # Dates.intervals.append(finaltime)

                        db.session.add(Dates)

                    db.session.commit()
                return redirect(url_for("main.main_page"))
            elif request.form.get("chooseTool") == "chooseTool":
                if request.form.get("spaceName") == 'hide':
                    return render_template('default/reservation/space.html', reserve1=reserve, tools=tool, form=form)
                else:
                    name = request.form.get("spaceName")
                    val1 = name.split('&')

                    datetime1 = request.form.get('datetimes')
                    return render_template('default/reservation/space_with_tool.html', id=int(val1[0]),
                                           reserve1=reserve, tools=tool, name=val1[2], datetime=datetime1,
                                           price=val1[1], form=form)

            elif request.form.get("confirmWithTool") == "confirmWithTool":
                name = request.form.get("toolName")
                val = name.split('&')
                user_id = current_user.get_id()
                space = Reservation(
                    # reservation for Space
                    space_id=val[0],
                    type="space",
                    payment_status="no_payment",
                    user_id=user_id,
                    full_price=val[1],
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
                    days = int(start_date[1])
                    counter = int(end_date[1]) - int(start_date[1])
                    if start_date[0] == end_date[0] and start_date[2] == end_date[2]:
                        for count in range(counter + 1):
                            final_date = start_date[2] + "-" + \
                                start_date[0] + "-" + str(days)
                            days += 1
                            Dates = Calendar(
                                day=final_date
                            )
                            ##############################################################
                            db.session.add(Dates)
                        db.session.commit()
                    ########## Save no_ Range_date ###########################
                elif date_no_range != "":
                    dates = date_no_range.split(", ")
                    for final_date in dates:
                        Dates = Calendar(
                            day=final_date
                        )
                        db.session.add(Dates)
                        time1 = request.form.get("time_picker_no_range")
                        time2 = request.form.get("time2_picker_no_range")
                        ftime = time1.split(" ")
                        etime = time2.split(" ")
                        Time1 = int(ftime[0])
                        Time2 = int(etime[0])
                        if ftime[1] == "م":
                            Time1 += 12
                        if etime[1] == "م":
                            Time2 += 12
                        finaltime = Interval(
                            start_time=str(Time1) + ":00:00",
                            end_time=str(Time2) + ":00:00",
                        )
                        db.session.add(finaltime)

                    tools = Reservation(
                        tool_id=val[2],
                        type="tool",
                        payment_status="no_payment",
                        user_id=user_id,
                        full_price=val[3]
                    )
                    db.session.add(tools)
                    db.session.commit()
                    return redirect(url_for("main.main_page"))
            if request.form.get("cancel") == "cancel":
                return redirect(url_for("main.main_page"))
        return render_template('/default/reservation/space.html', reserve1=reserve, tools=tool, form=form)
    elif current_user.role.name == "admin":
        return redirect(url_for("dashboard.reservation.create_reservation_space"))
