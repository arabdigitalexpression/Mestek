from flask_wtf import FlaskForm
from wtforms import (
    StringField, SelectField, HiddenField,
    BooleanField, FloatField, Form,
)
from wtforms.widgets import ColorInput
from wtforms.validators import (
    DataRequired, Length, NumberRange
)

from app.enums import PriceUnit

images = 'jpg jpe jpeg png gif svg bmp webp'.split()


class ColorField (StringField):
    widget = ColorInput()


class RoleCategoryForm(FlaskForm):
    name = StringField(
        'الاسم', validators=[DataRequired(), Length(max=50)],
        render_kw={
            "class": "form-control",
        }
    )
    desc = StringField(
        'الوصف', validators=[Length(max=128)],
        render_kw={
            "class": "form-control",
        }
    )
    colorCode = ColorField(
        'اللون', validators=[DataRequired(), Length(max=10)],
        render_kw={
            "class": "form-control form-control-color", "title": "Choose your color"
        }
    )
    isOrganization = BooleanField("منظمة", default=False, render_kw={
        "class": "form-check-input"
    })


class ConfirmForm(FlaskForm):
    value = StringField(
        '', validators=[DataRequired(), Length(max=50)],
        render_kw={
            "class": "form-control",
        }
    )


class PriceListForm(Form):
    category_id = HiddenField()
    price = FloatField(
        'السعر', validators=[DataRequired(), NumberRange(min=0)], render_kw={
            "placeholder": "السعر", "class": "form-control",
        }
    )
    price_unit = SelectField(
        'العملة', render_kw={"class": "form-select"},
        choices=[
            (PriceUnit.egp, PriceUnit.egp.description),
            (PriceUnit.usd, PriceUnit.usd.description)
        ]
    )