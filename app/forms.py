from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, email


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