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

from app.models import User

images = 'jpg jpe jpeg png gif svg bmp webp'.split()


class RoleCategoryForm(FlaskForm):
    name = StringField(
        'الاسم', validators=[DataRequired(), Length(max=50)],
        render_kw={
            "class": "form-control rounded-0",
        }
    )
    colorCode = StringField(
        'اللون', validators=[DataRequired(), Length(max=10)],
        render_kw={
            "class": "form-control rounded-0", "title": "Choose your color"
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


class EditUserForm(FlaskForm):
    firstName = StringField('الاسم الأول', validators=[DataRequired(), Length(min=3, max=20)],
                            render_kw={
                                "class": "form-control rounded-0 my-2",
                            })
    lastName = StringField('الاسم الأخير', validators=[DataRequired(), Length(min=3, max=20)],
                           render_kw={
                               "class": "form-control rounded-0 my-2",
                           })
    userName = StringField('إسم المستخدم', validators=[DataRequired(), Length(min=3, max=20)],
                           render_kw={
                               "class": "form-control rounded-0 my-2",
                           })
    email = EmailField('البريد الإلكترونى', validators=[DataRequired()],
                       render_kw={
                           "class": "form-control rounded-0 my-2",
                       })
    submit = SubmitField('تعديل',
                         render_kw={
                             "class": "btn btn-dark rounded-0 my-3",
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
                                 "class": "form-control rounded-0 my-2",
                             })
    password = PasswordField('كلمة المرور الجديدة', validators=[DataRequired(), Length(min=6, max=20)],
                             render_kw={
                                 "class": "form-control rounded-0 my-2",
                             })
    confirm_password = PasswordField('تأكيد كلمة المرور', validators=[DataRequired(), EqualTo('password')],
                                     render_kw={
                                         "class": "form-control rounded-0 my-2",
                                     })
    submit = SubmitField('حفظ',
                         render_kw={
                             "class": "btn btn-dark rounded-0 my-3",
                         })


class SpaceForm(FlaskForm):
    name = StringField(
        'أسم المساحة', validators=[DataRequired(), Length(max=50)],
        render_kw={
            "placeholder": "أسم المساحة", "class": "form-control rounded-0",
        }
    )
    price = FloatField('السعر', validators=[DataRequired()],
                       render_kw={
        "placeholder": "السعر", "class": "form-control rounded-0",
    })
    has_operator = BooleanField('مشرف؟',
                                render_kw={
                                    "class": "form-check-input"
                                }
                                )
    description = TextAreaField('الوصف', validators=[DataRequired(), Length(max=128)],
                                render_kw={
        "placeholder": "الوصف", "class": "form-control rounded-0", "rows": "5"
    }
    )
    guidelines = TextAreaField('قواعد', validators=[DataRequired(), Length(max=256)],
                               render_kw={
        "placeholder": "قواعد", "class": "form-control rounded-0", "rows": "5"
    }
    )
    images = MultipleFileField('الصور', name="images", validators=[
        # FileRequired(),
        FileAllowed(images, 'الرجاء إدخال صور فقط!')
    ], render_kw={
        "class": "form-control rounded-0"
    }
    )


class ToolForm(FlaskForm):
    name = StringField('أسم اﻹداة', validators=[DataRequired(), Length(max=50)],
                       render_kw={
        "placeholder": "أسم اﻹداة", "class": "form-control rounded-0",
    })
    price = FloatField('السعر', validators=[DataRequired()],
                       render_kw={
        "placeholder": "السعر", "class": "form-control rounded-0",
    })
    has_operator = BooleanField('مشرف؟',
                                render_kw={
                                    "class": "form-check-input"
                                })
    description = TextAreaField('الوصف', validators=[DataRequired(), Length(max=128)],
                                render_kw={
        "placeholder": "الوصف", "class": "form-control rounded-0", "rows": "5"
    })
    guidelines = TextAreaField('قواعد', validators=[DataRequired(), Length(max=256)],
                               render_kw={
        "placeholder": "قواعد", "class": "form-control rounded-0", "rows": "5"
    })
    space = SelectField('المساحة', render_kw={
        "class": "form-select",
    })
    images = MultipleFileField('الصور', name="images", validators=[
        # FileRequired(),
        FileAllowed(images, 'الرجاء إدخال صور فقط!')
    ], render_kw={
        "class": "form-control rounded-0"
    })


class ConfirmForm(FlaskForm):
    value = StringField(
        '', validators=[DataRequired(), Length(max=50)],
        render_kw={
            "class": "form-control rounded-0",
        }
    )


# class reserveTool(FlaskForm):
#     name =