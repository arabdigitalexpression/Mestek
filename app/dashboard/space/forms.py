from flask_wtf import FlaskForm
from wtforms import (
    StringField, FloatField, BooleanField, TextAreaField,
    FieldList, IntegerField, SubmitField, SelectField,
    FormField, Form,
)
from wtforms.validators import (
    DataRequired, Length, NumberRange,
)
from wtforms.fields import MultipleFileField
from flask_wtf.file import FileAllowed

from app.dashboard.forms import PriceListForm, images
from app.enums import SpaceUnit


class SpaceCategoryPriceForm(Form):
    unit_value = FloatField(
        'القيمة', validators=[DataRequired(), NumberRange(min=0)], render_kw={
            "placeholder": "القيمة", "class": "form-control form-control-sm rounded-0",
        }
    )
    unit = SelectField(
        'الوحدة', validators=[DataRequired()],
        render_kw={"class": "form-select form-select-sm rounded-0"},
        choices=[
            (SpaceUnit.hour, SpaceUnit.hour.description),
            (SpaceUnit.day, SpaceUnit.day.description)
        ]
    )
    price_list = FieldList(FormField(PriceListForm))



class SpaceForm(FlaskForm):
    name = StringField(
        'أسم المساحة', validators=[DataRequired(), Length(max=50)],
        render_kw={

            "placeholder": "أسم المساحة", "class": "form-control form-control-sm rounded-0",
        }
    )
    has_operator = BooleanField('مشرف؟',
                                render_kw={
                                    "class": "form-check-input"
                                }
                                )

    description = TextAreaField('الوصف', validators=[Length(max=1024)],

                                render_kw={
        "placeholder": "الوصف", "class": "form-control form-control-sm rounded-0", "rows": "5", "id": "description"})
    capacity = IntegerField('السعة', validators=[DataRequired()],
                            render_kw={
        "placeholder": "السعة", "class": "form-control form-control-sm rounded-0",
    })

    guidelines = TextAreaField('قواعد',
                               render_kw={
                                   "placeholder": "قواعد", "class": "form-control form-control-sm rounded-0", "rows": "5", "id": "guidelines"
                               }
                               )
    images = MultipleFileField(
        'الصور', name="images", validators=[  # FileRequired(),
            FileAllowed(images, 'الرجاء إدخال صور فقط!')

        ], render_kw={"class": "form-control form-control-sm rounded-0"})
    category_prices = FieldList(FormField(SpaceCategoryPriceForm))
    add_new_price = SubmitField('إضافة تسعيرة جديدة', render_kw={
        "class": "btn btn-sm btn-dark btn-sm rounded-0"})

