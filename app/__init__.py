from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)

app.config["SECRET_KEY"] = "you-will-never-guess"

# The Sqlite database file is in '../test.db' relative path
# 'sqlite://' is database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../test.db"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import models, controllers, forms