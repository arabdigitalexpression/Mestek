from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import (
    StringField, SubmitField, SelectField, FileField, TextAreaField)
from wtforms.validators import (
    DataRequired, Length, )

from app.models import Category

images = 'jpg jpe jpeg png gif svg bmp webp'.split()


class OrganizationForm(FlaskForm):
    name = StringField('اسم المؤسسة', validators=[DataRequired(), Length(min=3, max=20)],
                       render_kw={
                           "class": "form-control ",
                       })
    description = TextAreaField('الوصف', validators=[Length(min=3, max=2048)],
                                render_kw={
                                    "class": "form-control ",
                                    "placeholder": "الوصف",
                                    "id": "desc",
                                    "rows": "4"
                                })
    address = StringField('العنوان', validators=[Length(max=512)],
                          render_kw={
                              "class": "form-control",
                              "placeholder": "العنوان"
                          })
    website_url = StringField('الموقع الإلكترونى', validators=[Length(max=128)],
                              render_kw={
                                  "class": "form-control",
                                  "placeholder": "الموقع الإلكترونى"
                              })
    phone = StringField('الهاتف', validators=[Length(max=32)],
                        render_kw={
                            "class": "form-control",
                            "placeholder": "الهاتف"
                        })
    category = SelectField('التصنيف', validators=[DataRequired()],
                           choices=[(c.id, c.name) for c in Category.query.filter_by(is_organization=True)].insert(0, (
                               0, "-- اختر تصنيف --")),
                           render_kw={
                               "class": "form-select",
                               "placeholder": "النوع"
                           })
    logo_url = FileField('شعار المؤسسة', name="images", validators=[
        FileAllowed(images, 'الرجاء إدخال صور فقط!')
    ], render_kw={
        "class": "form-control"
    })
    submit = SubmitField('تسجيل المؤسسة',
                         render_kw={
                             "class": "w-100 btn btn-lg btn-primary",
                         })
