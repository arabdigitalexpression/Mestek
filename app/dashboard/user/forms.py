from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, EmailField,
    SubmitField, SelectField,
)
from wtforms.validators import (
    DataRequired, Length, EqualTo,
)


class UserCreateForm(FlaskForm):
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
