import os
from flask import current_app
from app.config import basedir
from app import create_app

def test_app_is_development():
    app = create_app('dev')
    assert app.config["DEBUG"] is True
    # Default URI check
    expected_uri = os.getenv("DATABASE_URL", "sqlite:///" + os.path.join(basedir, "ticket_booking_main.db"))
    assert app.config["SQLALCHEMY_DATABASE_URI"] == expected_uri

def test_app_is_testing():
    app = create_app('test')
    assert app.config["DEBUG"] is True
    assert app.config["TESTING"] is True
    assert app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite:///" + os.path.join(basedir, "ticket_booking_test.db")

def test_app_is_production():
    app = create_app('prod')
    assert app.config["DEBUG"] is False
