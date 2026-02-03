import json

from flask import request
from flask_restx import Resource

from app.services.ticket_service import (book_a_ticket, delete_a_ticket,
                                         tickets_with_date_time,
                                         update_a_ticket,
                                         user_details_from_ticket_id)

from app.utils.dto import TicketDto, UserDto

api = TicketDto.api
user_api = UserDto.api
_ticket = TicketDto.ticket
_ticket_book = TicketDto.ticket_book
_ticket_update = TicketDto.ticket_update
_user = UserDto.user


@api.route("/")
class BookTicket(Resource):
    @api.response(201, "Ticket booked successfully.")
    @api.doc("Book a new ticket")
    @api.expect(_ticket_book, validate=True)
    def post(self):
        """Books a new Ticket """
        data = request.json
        return book_a_ticket(data=data)

    @api.response(201, "Ticket updated successfully.")
    @api.doc("Update a ticket's timing")
    @api.expect(_ticket_update, validate=False)
    def put(self):
        """Updates a existing Ticket"""
        data = json.loads(request.data)
        return update_a_ticket(data=data)

    @api.response(201, "Ticket deleted successfully.")
    @api.doc("Delete a ticket")
    @api.expect(_ticket_update, validate=False)
    def delete(self):
        """Deletes a ticket"""
        data = request.json
        return delete_a_ticket(data=data)

    @api.doc("list of tickets with particular time and date")
    @api.marshal_list_with(_ticket, envelope="tickets")
    @api.param("movie_id", "The id of the movie")
    @api.param("date", "The date of the movie")
    @api.param("time_id", "The id of the time slot for the movie")
    def get(self):
        """list of tickets with particular time and date"""
        data = request.args
        return tickets_with_date_time(data)


@api.route("/u/<ticket_id>")
@api.param("ticket_id", "The id of the ticket to get information of")
class ShowTicketUser(Resource):
    @api.doc("user details from ticket Id")
    @api.marshal_with(_user, envelope="user")
    def get(self, ticket_id):
        """list of tickets with particular time and date"""
        return user_details_from_ticket_id(ticket_id)
