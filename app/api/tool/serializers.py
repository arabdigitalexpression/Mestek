from webargs import fields, validate

from app.enums import (
    PaymentTypes,  # ReservationTypes
)

tool_reservation_args = {
    "description": fields.Str(required=True),
    "tool_id": fields.Int(required=True),
    "tool_price_id": fields.Int(required=True),
    "days_only": fields.Boolean(required=True),
    "days": fields.List(fields.DateTime(), required=True),
    "payment_status": fields.Enum(PaymentTypes),
    "from_time": fields.DateTime(),
    "to_time": fields.DateTime(),
}