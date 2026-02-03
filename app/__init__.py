import os
from flask import Flask, Blueprint
from flask_restx import Api
from apscheduler.schedulers.background import BackgroundScheduler

from app.extensions import db, migrate, flask_bcrypt
from app.config import config_by_name


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    db.init_app(app)
    migrate.init_app(app, db)
    flask_bcrypt.init_app(app)

    # Register Blueprint and API
    blueprint = Blueprint("api", __name__, url_prefix="/api")
    api = Api(
        blueprint,
        title="Ticket Booking App",
        version="1.0",
        description="An API for Ticket Booking",
        doc="/doc"
    )

    # Import namespaces here to avoid circular imports
    from app.api.ticket_controller import api as ticket_ns
    from app.api.ticket_controller import user_api as user_ns

    api.add_namespace(ticket_ns, path='/ticket')
    api.add_namespace(user_ns, path='/user')

    app.register_blueprint(blueprint)

    # Scheduler configuration
    if not app.debug or os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        from app.utils.cron import set_ticket_expired, delete_expired_ticket
        scheduler = BackgroundScheduler()
        scheduler.add_job(set_ticket_expired, trigger='interval', seconds=1*60*60)
        scheduler.add_job(delete_expired_ticket, trigger='interval', seconds=24*60*60)
        scheduler.start()

        # Shut down the scheduler when exiting the app
        import atexit
        atexit.register(lambda: scheduler.shutdown())

    return app
