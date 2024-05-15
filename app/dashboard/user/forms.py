from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import (
    StringField, PasswordField, EmailField,
    SubmitField, SelectField, DateField, BooleanField,
)
from wtforms.validators import (
    DataRequired, Length, EqualTo,
)

from app.enums import Gender

images = 'jpg jpe jpeg png gif svg bmp webp'.split()


class CreateUserForm(FlaskForm):
    firstName = StringField('الاسم الأول', validators=[DataRequired(), Length(min=3, max=20)],
                            render_kw={
                                "class": "form-control ",
                            })
    lastName = StringField('الاسم الأخير', validators=[DataRequired(), Length(min=3, max=20)],
                           render_kw={
                               "class": "form-control ",
                           })
    userName = StringField('إسم المستخدم', validators=[DataRequired(), Length(min=3, max=20)],
                           render_kw={
                               "class": "form-control ",
                           })
    email = EmailField('البريد الإلكترونى', validators=[DataRequired()],
                       render_kw={
                           "class": "form-control ",
                       })
    address = StringField('العنوان', validators=[Length(min=2)],
                          render_kw={
                              "class": "form-control",
                              "placeholder": "العنوان"
                          })
    website_url = StringField('الموقع الإلكترونى', validators=[Length(min=3)],
                              render_kw={
                                  "class": "form-control",
                                  "placeholder": "الموقع الإلكترونى"
                              })
    phone = StringField('الهاتف', validators=[DataRequired(), Length(min=3, max=20)],
                        render_kw={
                            "class": "form-control",
                            "placeholder": "الهاتف"
                        })
    gender = SelectField('الجنس', choices=Gender.choices(),
                         render_kw={
                             "class": "form-control",
                             "placeholder": "النوع"
                         })
    birthday = DateField('تاريخ الميلاد', validators=[DataRequired()],
                         render_kw={
                             "class": "form-control",
                             "placeholder": "تاريخ الميلاد"
                         })
    avatar_url = FileField('الصورة الشخصية', name="avatar", validators=[
        FileAllowed(images, 'الرجاء إدخال صور فقط!')
    ], render_kw={
        "class": "form-control"
    })
    password = PasswordField('كلمة المرور', validators=[DataRequired(), Length(min=6, max=20)],
                             render_kw={
                                 "class": "form-control ",
                             })
    confirm_password = PasswordField('تأكيد كلمة المرور', validators=[DataRequired(), EqualTo('password')],
                                     render_kw={
                                         "class": "form-control ",
                                     })
    role = SelectField('الصلاحية', render_kw={
        "class": "form-select ",
    })
    category = SelectField('التصنيف', render_kw={
        "class": "form-select ",
    })
    activated = BooleanField('مفعل',
                             render_kw={
                                 "class": "form-check-input"
                             })
    submit = SubmitField('تسجيل الحساب',
                         render_kw={
                             "class": "w-100 btn btn-lg btn-primary",
                         })


class UpdateUserForm(CreateUserForm):
    organization = SelectField('المؤسسة', render_kw={
        "class": "form-select ",
    })


class ChangePasswordForm(FlaskForm):
    password = PasswordField('كلمة المرور الجديدة', validators=[DataRequired(), Length(min=6, max=20)],
                             render_kw={
                                 "class": "form-control my-2",
                             })
    confirm_password = PasswordField('تأكيد كلمة المرور', validators=[DataRequired(), EqualTo('password')],
                                     render_kw={
                                         "class": "form-control my-2",
                                     })
    submit = SubmitField('تغيير كلمة المرور',
                         render_kw={
                             "class": "btn btn-primary my-3",
                         })
