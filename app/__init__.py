from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

import pymysql
connection = pymysql.connect(host='localhost', user='adefsrs', password='Adef@SRS2022',
                             database='adef_srs', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

app = Flask(__name__)

app.config["SECRET_KEY"] = "you-will-never-guess"

app.config['MAX_CONTENT_LENGTH'] = 8 * 1000 * 1000
app.config["UPLOAD_PATH"] = "uploads"
app.config["APP_PATH"] = app.root_path

# The Sqlite database file is in '../test.db' relative path
# 'sqlite:///' is database with '../test.db' is the project directory
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://adefsrs:Adef%40SRS2022@localhost/adef_srs"
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
# force users to login if they visited protected page
# that needs authentication
login.login_view = "auth.login_page"


from app.main import bp as main_bp
from app.main.profile import bp as profile_main_bp
from app.main.reservation import bp as reservation_main_bp
main_bp.register_blueprint(profile_main_bp)
main_bp.register_blueprint(reservation_main_bp)
app.register_blueprint(main_bp)

from app.dashboard import bp as dashboard_bp
from app.dashboard.reservation import bp as reservation_dashboard_bp
from app.dashboard.space import bp as space_dashboard_bp
from app.dashboard.tool import bp as tool_dashboard_bp
from app.dashboard.role import bp as role_dashboard_bp
from app.dashboard.category import bp as category_dashboard_bp
from app.dashboard.user import bp as user_dashboard_bp
dashboard_bp.register_blueprint(reservation_dashboard_bp)
dashboard_bp.register_blueprint(space_dashboard_bp)
dashboard_bp.register_blueprint(tool_dashboard_bp)
dashboard_bp.register_blueprint(role_dashboard_bp)
dashboard_bp.register_blueprint(category_dashboard_bp)
dashboard_bp.register_blueprint(user_dashboard_bp)
app.register_blueprint(dashboard_bp)

from app.auth import bp as auth_bp
app.register_blueprint(auth_bp)

from app.api import bp as api_bp
app.register_blueprint(api_bp)


from app import models
