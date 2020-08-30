from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from .config import config_by_name

db = SQLAlchemy()
flask_bcrypt = Bcrypt()

from app.main.util.cron import set_ticket_expired, delete_expired_ticket


def create_app(config_name):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    flask_bcrypt.init_app(app)
    scheduler = BackgroundScheduler()
    scheduler.add_job(set_ticket_expired, trigger='interval', seconds=1*60*60)
    scheduler.add_job(delete_expired_ticket, trigger='interval', seconds=24*60*60)
    scheduler.start()
    try:
        return app
    except:
        scheduler.shutdown()
