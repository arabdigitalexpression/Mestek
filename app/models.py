from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from datetime import datetime

from app import db, login


# the login extension register this load_user function
# it executes it when someone send a request to our app
# the user_loader decorator passes the id as string
# so we convert it to int
@login.user_loader
def load_user(id):
    return User.query.get(int(id))


# The UserMixin adds stuff for us like is_authenticated property
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password = db.Column(db.String(128), nullable=False)

    role = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)

    # created at date when user registered
    # Date is year-month-day
    # Time Hour:Minute:Second nano timezone
    created_at = db.Column(
        db.DateTime(), default=datetime.utcnow(),
        nullable=False
        )

    def __repr__(self):
        return '<User %r>' % self.username

    
    def make_password(self, password):
        self.password = generate_password_hash(password)

    
    def verify_password(self, password):
        hashed_form_password = generate_password_hash(password)
        return self.password == hashed_form_password

    def save(self):
        db.session.add(self)
        db.session.commit()

    # TODO: Revisit this code
    # def update(self):
    #     pass


