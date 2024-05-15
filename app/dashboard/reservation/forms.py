from flask_wtf import FlaskForm
from wtforms import (
    StringField, FloatField, SelectField
)
from wtforms.validators import (
    DataRequired, Length, NumberRange
)


class ReservationUpdateForm(FlaskForm):
    transaction_num = StringField(
        'رقم المعاملة البنكية', render_kw={"class": "form-control"},
        validators=[DataRequired(), Length(max=128)]
    )
    payment_status = SelectField(
        'حالة الدفع', render_kw={"class": "form-select"}
    )
    discount = FloatField(
        'الخصم', validators=[NumberRange(min=0)],
        render_kw={"placeholder": "الخصم", "class": "form-control"}
    )
