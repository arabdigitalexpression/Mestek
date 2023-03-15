from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SECRET_KEY"] = "you-will-never-guess"

app.config['MAX_CONTENT_LENGTH'] = 8 * 1000 * 1000
app.config["UPLOAD_PATH"] = "uploads"
app.config["APP_PATH"] = app.root_path

# The Sqlite database file is in '../test.db' relative path
# 'sqlite:///' is database with '../test.db' is the project directory
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://adefsrs:pass_123@localhost/adef_srs"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
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
from app.dashboard.organization import bp as organization_dashboard_bp

dashboard_bp.register_blueprint(reservation_dashboard_bp)
dashboard_bp.register_blueprint(space_dashboard_bp)
dashboard_bp.register_blueprint(tool_dashboard_bp)
dashboard_bp.register_blueprint(role_dashboard_bp)
dashboard_bp.register_blueprint(category_dashboard_bp)
dashboard_bp.register_blueprint(user_dashboard_bp)
dashboard_bp.register_blueprint(organization_dashboard_bp)
app.register_blueprint(dashboard_bp)

from app.auth import bp as auth_bp

app.register_blueprint(auth_bp)

from app.api import bp as api_bp
from app.api.space import bp as space_api_bp
from app.api.tool import bp as tool_api_bp
from app.api.reservation import bp as reservation_api_bp

api_bp.register_blueprint(space_api_bp)
api_bp.register_blueprint(tool_api_bp)
api_bp.register_blueprint(reservation_api_bp)
app.register_blueprint(api_bp)

from app import models
