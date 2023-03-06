from webargs import fields, validate

# from app.enums import ReservationTypes

space_reservation_args = {
    "description": fields.Str(required=True),
    "attendance_num": fields.Int(),
    "min_age": fields.Int(),
    "max_age": fields.Int(),
    "space_id": fields.Int(required=True),
    "space_price_id": fields.Int(required=True),
    "tools": fields.List(fields.Int()),
    "days_only": fields.Boolean(required=True),
    "days": fields.List(fields.DateTime(), required=True),
    "from_time": fields.DateTime(),
    "to_time": fields.DateTime(),
}
