from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, EmailField, SubmitField,
    FloatField, BooleanField, TextAreaField, SelectField
)
from wtforms.validators import (
    DataRequired, Length, EqualTo, email
)
from wtforms.fields import MultipleFileField
from flask_wtf.file import FileAllowed, FileRequired


images = 'jpg jpe jpeg png gif svg bmp webp'.split()


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
    firstName = StringField('الاسم الأول', validators=[DataRequired(),Length(min=3,max=20)],
        render_kw={
             "class": "form-control rounded-0",
        })
    lastName = StringField('الاسم الأخير', validators=[DataRequired(),Length(min=3,max=20)],
        render_kw={
            "class": "form-control rounded-0",
        })
    userName = StringField('إسم المستخدم', validators=[DataRequired(),Length(min=3,max=20)],
        render_kw={
            "class": "form-control rounded-0",
        })
    email= EmailField('البريد الإلكترونى',validators=[DataRequired()],
        render_kw={
            "class": "form-control rounded-0",
        })
    password = PasswordField('كلمة المرور', validators=[DataRequired(),Length(min=6,max=20)],
        render_kw={
            "class": "form-control rounded-0",
        })
    confirm_password = PasswordField('تأكيد كلمة المرور', validators=[DataRequired(),EqualTo('password')],
        render_kw={
            "class": "form-control rounded-0",
        })
    submit= SubmitField('تسجيل الحساب',
        render_kw={
            "class": "w-100 btn btn-lg btn-dark rounded-0",
        })


class SpaceForm(FlaskForm):
    name = StringField(
        'أسم المساحة', validators=[DataRequired(), Length(max=50)],
        render_kw={
            "placeholder":"أسم المساحة", "class": "form-control",
            "style": "height: 50px;"
        }
    )
    price = FloatField('السعر', validators=[DataRequired()],
        render_kw={
            "placeholder":"السعر", "class": "form-control",
            "style": "height: 50px;"
        })
    has_operator = BooleanField('مشرف؟',
        render_kw={
            "class": "form-check-input"
        }
    )
    description = TextAreaField('الوصف', validators=[DataRequired(), Length(max=128)],
        render_kw={
            "placeholder":"الوصف", "class": "form-control",
            "style": "height: 150px; margin-top: -20px;"
        }
    )
    guidelines = TextAreaField('قواعد', validators=[DataRequired(), Length(max=256)],
        render_kw={
            "placeholder":"قواعد", "class": "form-control",
            "style": "height: 150px; margin-top: -20px;"
        }
    )
    images = MultipleFileField('الصور', name="images", validators=[
        # FileRequired(),
        FileAllowed(images, 'الرجاء إدخال صور فقط!')
    ], render_kw={
        "class": "form-control"
    }
    )


class ToolForm(FlaskForm):
    name = StringField('أسم اﻹداة', validators=[DataRequired(), Length(max=50)])
    price = FloatField('السعر', validators=[DataRequired()])
    has_operator = BooleanField('مشرف؟')
    description = TextAreaField('الوصف', validators=[DataRequired(), Length(max=128)])
    guidelines = TextAreaField('قواعد', validators=[DataRequired(), Length(max=256)])
    space = SelectField('المساحة')
    images = MultipleFileField('الصور', name="images", validators=[
        # FileRequired(),
        FileAllowed(images, 'الرجاء إدخال صور فقط!')
    ])
