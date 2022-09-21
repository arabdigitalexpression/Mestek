from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)

app.config["SECRET_KEY"] = "you-will-never-guess"

app.config['MAX_CONTENT_LENGTH'] = 8 * 1000 * 1000
app.config["UPLOAD_PATH"] = "uploads"
app.config["APP_PATH"] = app.root_path

# The Sqlite database file is in '../test.db' relative path
# 'sqlite:///' is database with '../test.db' is the project directory
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost/srs"
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
# force users to login if they visited protected page
# that needs authentication
login.login_view = "login_page"

from app import models, controllers, forms