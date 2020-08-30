
# app/__init__.py

from flask import Blueprint
from flask_restplus import Api

from app.main.controller.ticket_controller import api as ticket_ns
from app.main.controller.ticket_controller import user_api as user_ns

blueprint = Blueprint("api", __name__)

api = Api(
    blueprint,
    title="Ticket Booking App",
    version="1.0",
    description="an api for Ticket Booking",
)

api.add_namespace(ticket_ns, path='/ticket')
api.add_namespace(user_ns, path='/user')
