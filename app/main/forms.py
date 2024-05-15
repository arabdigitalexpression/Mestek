from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, EmailField, SubmitField,
    SelectField
)
from wtforms.validators import (
    DataRequired, Length, EqualTo, email
)
