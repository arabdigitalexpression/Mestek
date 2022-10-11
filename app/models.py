import enum
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
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
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password = db.Column(db.String(128), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey(
        'category.id'), nullable=False)

    # created at date when user registered
    # Date is year-month-day
    # Time Hour:Minute:Second nano timezone
    created_at = db.Column(
        db.DateTime(), default=datetime.utcnow(),
        nullable=False
    )

    reservations = db.relationship('Reservation', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.username

    def make_password(self, password):
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def save(self):
        db.session.add(self)
        db.session.commit()

    # TODO: Revisit this code
    # def update(self):
    #     pass


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    color_code = db.Column(db.String(10), unique=True, nullable=False)
    users = db.relationship('User', backref='role', lazy=True)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    color_code = db.Column(db.String(10), unique=True, nullable=False)
    users = db.relationship('User', backref='category', lazy=True)


class Space(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text(1024), nullable=False)
    guidelines = db.Column(db.String(1024), nullable=False)
    has_operator = db.Column(db.Boolean, default=False, nullable=False)
    price = db.Column(db.Float, nullable=False)
    images = db.relationship('Image', backref='space', lazy=True)
    reservations = db.relationship(
        'Reservation', cascade="all", backref='space', lazy=True)
    tools = db.relationship('Tool', backref='space', lazy=True)


class Tool(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(1024), nullable=False)
    guidelines = db.Column(db.String(1024), nullable=False)
    has_operator = db.Column(db.Boolean, default=False, nullable=False)
    price = db.Column(db.Float, nullable=False)
    images = db.relationship('Image', backref='tool', lazy=True)
    reservations = db.relationship(
        'Reservation', cascade="all", backref='tool', lazy=True)
    space_id = db.Column(db.Integer, db.ForeignKey('space.id'), nullable=True)


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(128), nullable=False)
    space_id = db.Column(db.Integer, db.ForeignKey('space.id'), nullable=True)
    tool_id = db.Column(db.Integer, db.ForeignKey('tool.id'), nullable=True)


class ReservationTypes(enum.Enum):
    space = 0
    tool = 1


class PaymentTypes(enum.Enum):
    no_payment = 0
    down_payment = 1
    full_payment = 2


reservation_calendar = db.Table(
    'reservation_calendar', db.Model.metadata,
    db.Column('reservation_id', db.Integer, db.ForeignKey('reservation.id')),
    db.Column('calendar_id', db.Integer, db.ForeignKey('calendar.id'))
)

reservation_tool = db.Table(
    'reservation_tool', db.Model.metadata,
    db.Column('reservation_id', db.Integer, db.ForeignKey('reservation.id')),
    db.Column('tool_id', db.Integer, db.ForeignKey('tool.id'))
)

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Enum(ReservationTypes), nullable=False)
    payment_status = db.Column(db.Enum(PaymentTypes), nullable=False)
    transaction_num = db.Column(db.String(128))
    created_at = db.Column(
        db.DateTime(), default=datetime.utcnow(),
        nullable=False
    )
    full_price = db.Column(db.Float, nullable=False)
    space_id = db.Column(db.Integer, db.ForeignKey('space.id'), nullable=True)
    calendars = db.relationship(
        'Calendar', secondary=reservation_calendar,
        backref=db.backref('reservations')
    )
    tools = db.relationship(
        'Tool', secondary=reservation_tool,
        backref=db.backref('reservations')
    )
    intervals = db.relationship('Interval', cascade="all, delete", backref='tool', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)


class Calendar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.Date(), nullable=False)
    intervals = db.relationship(
        'Interval', cascade="all, delete", backref='interval', lazy=True)


class Interval(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    calendar_id = db.Column(db.Integer, db.ForeignKey(
        'calendar.id', ondelete="CASCADE"), nullable=True)
    reservation_id = db.Column(db.Integer, db.ForeignKey(
        'reservation.id', ondelete="CASCADE"), nullable=True)
