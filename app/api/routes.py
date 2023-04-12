from flask import jsonify, abort
from flask_login import current_user, login_required

from app.api import bp
from app.models import (
    User,
    # Notification
)


@bp.route('users/', methods=['GET'])
@login_required
def users():
    if current_user.role.name != "admin":
        return abort(401)

    users = User.query.with_entities(
        User.id, User.email
    ).all()

    return jsonify([{
            "id": u.id, "email": u.email
        } for u in users
    ])


@bp.errorhandler(400)
def bad_req(error):
    response = jsonify({
        'code': 400,
        'message': 'حدث خطأ ما.',
        'error': error.description
    })
    response.status_code = 400
    return response


#
# @bp.route('notifications/', methods=['GET'])
# @login_required
# def notifications():
#     not_read = request.args.get("not_read", type=bool)
#     since = request.args.get("since", 0.0, type=float)
#
#     notifs = Notification.query.\
#         filter(Notification.timestamp > since).\
#         filter(Notification.user_id == current_user.id).\
#         order_by(Notification.timestamp.asc())
#
#     if not_read:
#         notifs.filter(Notification.is_read is None)
#
#     return jsonify([{
#         "id": n.id, "title": n.title, "body": n.body,
#         "datetime": datetime.fromtimestamp(n.timestamp)
#     } for n in notifs])
#
#
# @bp.route('notifications/read/<int:pk>/', methods=['GET'])
# @login_required
# def notifications(pk):
#     notif = Notification.query.get_or_404(pk)
#
#     if notif.user_id != current_user.id:
#         abort(400)
#
#
#     return jsonify([{
#         "id": n.id, "title": n.title, "body": n.body,
#         "datetime": datetime.fromtimestamp(n.timestamp)
#     } for n in notifs])
