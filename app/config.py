import os

# Project root directory
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


_SECRET_KEY = os.getenv("SECRET_KEY")
if _SECRET_KEY is None:
    raise RuntimeError("SECRET_KEY environment variable is required")


class Config:
    SECRET_KEY = _SECRET_KEY
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "sqlite:///" + os.path.join(basedir, "ticket_booking_main.db")
    )


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(
        basedir, "ticket_booking_test.db"
    )
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "sqlite:///" + os.path.join(basedir, "ticket_booking_prod.db")
    )


config_by_name = dict(dev=DevelopmentConfig, test=TestingConfig, prod=ProductionConfig)

key = Config.SECRET_KEY
