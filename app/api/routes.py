from flask import jsonify, abort
from flask_login import current_user, login_required

from app.api import bp
from app.models import (
    Reservation,
    # Notification
)

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
