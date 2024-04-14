from decouple import config

DATABASE_URI = config("DATABASE_URL")
if DATABASE_URI.startswith("postgres://"):
    DATABASE_URI = DATABASE_URI.replace("postgres://", "postgresql://", 1)


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = config("SECRET_KEY", default="guess-me-not")
    SECURITY_PASSWORD_SALT=config("SECURITY_PASSWORD_SALT", default="too-salty")
    MAILJET_API_KEY=config("MAILJET_API_KEY", default="mailjet-api-key")
    MAILJET_API_SECRET=config("MAILJET_API_SECRET", default="mailjet-api-secret")
    EMAIL_SENDER=config("EMAIL_SENDER", default="info@example.com")
    EMAIL_SENDER_NAME=config("EMAIL_SENDER_NAME", default="ADEF Team")
    MAX_CONTENT_LENGTH = 24 * 1000 * 1000
    SQLALCHEMY_DATABASE_URI = DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    WTF_CSRF_ENABLED = False
    DEBUG_TB_ENABLED = True


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///testdb.sqlite"
    BCRYPT_LOG_ROUNDS = 1
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    DEBUG = False
    DEBUG_TB_ENABLED = False
