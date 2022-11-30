from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import (
    StringField, EmailField, DateField, FileField,
    SubmitField, SelectField, PasswordField,
)
from wtforms.validators import (
    DataRequired, Length, EqualTo,
)

from app.models import User

images = 'jpg jpe jpeg png gif svg bmp webp'.split()


class EditUserForm(FlaskForm):
    firstName = StringField('الاسم الأول', validators=[DataRequired(), Length(min=3, max=20)],
                            render_kw={
                                "class": "form-control form-control-sm rounded-0 my-2",
                                "placeholder": "الاسم الأول"
    })
    lastName = StringField('الاسم الأخير', validators=[DataRequired(), Length(min=3, max=20)],
                           render_kw={
                               "class": "form-control form-control-sm rounded-0 my-2",
                               "placeholder": "الاسم الأخير"
    })
    userName = StringField('إسم المستخدم', validators=[DataRequired(), Length(min=3, max=20)],
                           render_kw={
                               "class": "form-control form-control-sm rounded-0 my-2",
                               "placeholder": "إسم المستخدم"
    })
    email = EmailField('البريد الإلكترونى', validators=[DataRequired()],
                       render_kw={
                           "class": "form-control form-control-sm rounded-0 my-2",
                           "placeholder": "البريد الإلكترونى"
    })
    address = StringField('العنوان', validators=[Length(min=2)],
                          render_kw={
        "class": "form-control form-control-sm rounded-0 my-2",
        "placeholder": "العنوان"
    })
    website_url = StringField('الموقع الإلكترونى', validators=[Length(min=3)],
                              render_kw={
        "class": "form-control form-control-sm rounded-0 my-2",
        "placeholder": "الموقع الإلكترونى"
    })
    phone = StringField('الهاتف', validators=[DataRequired(), Length(min=3, max=20)],
                        render_kw={
        "class": "form-control form-control-sm rounded-0 my-2",
        "placeholder": "الهاتف"
    })
    gender = SelectField('النوع', validators=[DataRequired(), Length(min=3, max=20)],
                         choices=['ذكر', 'أنثى', 'أرجو عدم التوضيح'],
                         render_kw={
        "class": "form-control form-control-sm rounded-0 my-2",
        "placeholder": "النوع"
    })
    birthday = DateField('تاريخ الميلاد', validators=[DataRequired(), Length(min=3, max=20)],
                         render_kw={
        "class": "form-control form-control-sm rounded-0 my-2",
        "placeholder": "تاريخ الميلاد"
    })
    avatar_url = FileField('الصورة الشخصية', name="images", validators=[
        FileAllowed(images, 'الرجاء إدخال صور فقط!')
    ], render_kw={
        "class": "form-control rounded-0"
    }
    )
    submit = SubmitField('تعديل البيانات',
                         render_kw={
                             "class": "btn btn-sm btn-dark rounded-0 my-3",
                         })

    def validate_on_submit(self):
        super().validate_on_submit()

        if self.userName.data and User.query\
                .filter(User.username == self.userName.data)\
                .count() <= 1:
            return True

        if self.email.data and User.query\
                .filter(User.email == self.email.data)\
                .count() <= 1:
            return True


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('كلمة المرور الحالية', validators=[DataRequired(), Length(min=6, max=20)],
                                     render_kw={
        "class": "form-control form-control-sm rounded-0 my-2",
    })
    password = PasswordField('كلمة المرور الجديدة', validators=[DataRequired(), Length(min=6, max=20)],
                             render_kw={
                                 "class": "form-control form-control-sm rounded-0 my-2",
    })
    confirm_password = PasswordField('تأكيد كلمة المرور', validators=[DataRequired(), EqualTo('password')],
                                     render_kw={
                                         "class": "form-control form-control-sm rounded-0 my-2",
    })
    submit = SubmitField('تغيير كلمة المرور',
                         render_kw={
                             "class": "btn btn-sm btn-dark rounded-0 my-3",
                         })

