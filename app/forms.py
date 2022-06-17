from flask_wtf import FlaskForm
from flask_uploads import UploadSet, IMAGES
from wtforms import (
    StringField, PasswordField, EmailField, SubmitField,
    FloatField, BooleanField, TextAreaField
)
from wtforms.validators import (
    DataRequired, Length, EqualTo, email
)
from flask_wtf.file import FileField, FileAllowed, FileRequired


images = UploadSet('images', IMAGES)


class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    
    # our own custom validator for the length
    def validate_user_is_unique(form, field):
        if len(field.data) > 0:
            return True
        return False


class SignupForm(FlaskForm):
    firstName = StringField('firstname', validators=[DataRequired(),Length(min=3,max=20)])
    lastName = StringField('lastname', validators=[DataRequired(),Length(min=3,max=20)])
    userName = StringField('username', validators=[DataRequired(),Length(min=3,max=20)])
    email= EmailField('email',validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired(),Length(min=6,max=20)])
    confirm_password = PasswordField('password', validators=[DataRequired(),EqualTo('password')])
    submit= SubmitField('تسجيل الحساب')


class CreateSpaceForm(FlaskForm):
    name = StringField('name', validators=[DataRequired(), Length(max=50)])
    price = FloatField('price', validators=[DataRequired()])
    has_operator = BooleanField('has operator', validators=[DataRequired()])
    description = TextAreaField('description', validators=[DataRequired(), Length(max=128)])
    guidelines = TextAreaField('guidelines', validators=[DataRequired(), Length(max=256)])
    images = FileField('images', validators=[
        FileRequired(),
        FileAllowed(images, 'Images only!')
    ])