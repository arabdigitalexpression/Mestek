from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, EmailField, SubmitField,
    SelectField
)
from wtforms.validators import (
    DataRequired, Length, EqualTo
)


class LoginForm(FlaskForm):
    username = StringField('إسم المستخدم', validators=[DataRequired()],
                           render_kw={
                               "class": "form-control form-control-user",
                               "placeholder": "إسم المستخدم"
                           })
    password = PasswordField('كلمة المرور', validators=[DataRequired()],
                             render_kw={
                                 "class": "form-control form-control-user",
                                 "placeholder": "كلمة المرور"

                             })

    # our own custom validator for the length
    def validate_user_is_unique(form, field):
        if len(field.data) > 0:
            return True
        return False


class SignupForm(FlaskForm):
    firstName = StringField('الاسم الأول', validators=[DataRequired(), Length(min=3, max=20)],
                            render_kw={
                                "class": "form-control form-control-user",
                                "placeholder": "الاسم الأول"
                            })
    lastName = StringField('الاسم الأخير', validators=[DataRequired(), Length(min=3, max=20)],
                           render_kw={
                               "class": "form-control form-control-user",
                               "placeholder": "الاسم الأخير"
                           })
    userName = StringField('إسم المستخدم', validators=[DataRequired(), Length(min=3, max=20)],
                           render_kw={
                               "class": "form-control form-control-user",
                               "placeholder": "إسم المستخدم"
                           })
    email = EmailField('البريد الإلكترونى', validators=[DataRequired()],
                       render_kw={
                           "class": "form-control form-control-user text-start",
                           "placeholder": "البريد الإلكترونى"
                       })
    password = PasswordField('كلمة المرور', validators=[DataRequired(), Length(min=6, max=20)],
                             render_kw={
                                 "class": "form-control form-control-user",
                                 "placeholder": "كلمة المرور"
                             })
    confirm_password = PasswordField('تأكيد كلمة المرور', validators=[DataRequired(), EqualTo('password')],
                                     render_kw={
                                         "class": "form-control form-control-user",
                                         "placeholder": "تأكيد كلمة المرور"
                                     })
    role = SelectField('الصلاحية', render_kw={
        "class": "form-select form-control-user",
    })
    category = SelectField('التصنيف', render_kw={
        "class": "form-select form-control-user p-3",
    })
    submit = SubmitField('تسجيل الحساب',
                         render_kw={
                             "class": "btn btn-primary btn-user btn-block",
                         })
