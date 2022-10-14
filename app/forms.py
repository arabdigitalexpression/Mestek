from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, EmailField, SubmitField,
    FloatField, BooleanField, TextAreaField, SelectField,
    Form, HiddenField, FieldList, FormField
)
from wtforms.validators import (
    DataRequired, Length, EqualTo, email
)
from wtforms.fields import MultipleFileField
from flask_wtf.file import FileAllowed, FileRequired

from app.enums import Unit, PriceUnit

images = 'jpg jpe jpeg png gif svg bmp webp'.split()


class RoleCategoryForm(FlaskForm):
    name = StringField(
        'الاسم', validators=[DataRequired(), Length(max=50)],
        render_kw={
            "class": "form-control",
        }
    )
    colorCode = StringField(
        'اللون', validators=[DataRequired(), Length(max=10)],
        render_kw={
            "class": "form-control", "title": "Choose your color"
        }
    )


class LoginForm(FlaskForm):
    username = StringField('البريد الإلكترونى', validators=[DataRequired()],
                           render_kw={
        "class": "form-control rounded-0",
    })
    password = PasswordField('كلمة المرور', validators=[DataRequired()],
                             render_kw={
        "class": "form-control rounded-0",
    })

    # our own custom validator for the length
    def validate_user_is_unique(form, field):
        if len(field.data) > 0:
            return True
        return False


class SignupForm(FlaskForm):
    firstName = StringField('الاسم الأول', validators=[DataRequired(), Length(min=3, max=20)],
                            render_kw={
        "class": "form-control rounded-0",
    })
    lastName = StringField('الاسم الأخير', validators=[DataRequired(), Length(min=3, max=20)],
                           render_kw={
        "class": "form-control rounded-0",
    })
    userName = StringField('إسم المستخدم', validators=[DataRequired(), Length(min=3, max=20)],
                           render_kw={
        "class": "form-control rounded-0",
    })
    email = EmailField('البريد الإلكترونى', validators=[DataRequired()],
                       render_kw={
        "class": "form-control rounded-0",
    })
    password = PasswordField('كلمة المرور', validators=[DataRequired(), Length(min=6, max=20)],
                             render_kw={
        "class": "form-control rounded-0",
    })
    confirm_password = PasswordField('تأكيد كلمة المرور', validators=[DataRequired(), EqualTo('password')],
                                     render_kw={
        "class": "form-control rounded-0",
    })
    role = SelectField('الصلاحية', render_kw={
        "class": "form-select rounded-0",
    })
    category = SelectField('التصنيف', render_kw={
        "class": "form-select rounded-0",
    })
    submit = SubmitField('تسجيل الحساب',
                         render_kw={
                             "class": "w-100 btn btn-lg btn-dark rounded-0",
                         })


class PriceListForm(Form):
    category_id = HiddenField()
    price = FloatField(
        'السعر', render_kw={
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


class CategoryPriceForm(Form):
    unit_value = FloatField(
        'القيمة', validators=[DataRequired()], render_kw={
            "placeholder": "القيمة", "class": "form-control",
        }
    )
    unit = SelectField(
        'الوحدة', validators=[DataRequired()],
        render_kw={"class": "form-select"},
        choices=[
            (Unit.hour, Unit.hour.description),
            (Unit.day, Unit.day.description)
        ]
    )
    price_list = FieldList(FormField(PriceListForm))


class SpaceForm(FlaskForm):
    name = StringField(
        'أسم المساحة', validators=[DataRequired(), Length(max=50)],
        render_kw={
            "placeholder": "أسم المساحة", "class": "form-control",
        }
    )
    price = FloatField('السعر', validators=[DataRequired()],
                       render_kw={
        "placeholder": "السعر", "class": "form-control",
    })
    has_operator = BooleanField('مشرف؟',
                                render_kw={
                                    "class": "form-check-input"
                                }
                                )
    description = TextAreaField('الوصف', validators=[Length(max=128)],
                                render_kw={
        "placeholder": "الوصف", "class": "form-control", "rows": "5", "id":"description"
    }
    )
    guidelines = TextAreaField('قواعد', 
                               render_kw={
        "placeholder": "قواعد", "rows": "5" , "id":"guidelines"
    }
    )
    category_prices = FieldList(FormField(CategoryPriceForm))
    images = MultipleFileField(
        'الصور', name="images", validators=[  # FileRequired(),
            FileAllowed(images, 'الرجاء إدخال صور فقط!')
        ], render_kw={"class": "form-control"}
    )
    add_new_price = SubmitField('إضافة تسعيرة جديدة')


class ToolForm(FlaskForm):
    name = StringField('أسم اﻹداة', validators=[DataRequired(), Length(max=50)],
                       render_kw={
        "placeholder": "أسم اﻹداة", "class": "form-control",
    })
    price = FloatField('السعر', validators=[DataRequired()],
                       render_kw={
        "placeholder": "السعر", "class": "form-control",
    })
    has_operator = BooleanField('مشرف؟',
                                render_kw={
                                    "class": "form-check-input"
                                })
    description = TextAreaField('الوصف', validators=[DataRequired(), Length(max=128)],
                                render_kw={
        "placeholder": "الوصف", "class": "form-control", "rows": "5", "id":"description"
    })
    guidelines = TextAreaField('قواعد', 
                               render_kw={
        "placeholder": "قواعد", "class": "form-control", "rows": "5" , "id":"guidelines"
    })
    space = SelectField('المساحة', render_kw={
        "class": "form-select",
    })
    images = MultipleFileField('الصور', name="images", validators=[
        # FileRequired(),
        FileAllowed(images, 'الرجاء إدخال صور فقط!')
    ], render_kw={
        "class": "form-control"
    })


class ConfirmForm(FlaskForm):
    value = StringField(
        '', validators=[DataRequired(), Length(max=50)],
        render_kw={
            "class": "form-control",
        }
    )


# class reserveTool(FlaskForm):
#     name = 