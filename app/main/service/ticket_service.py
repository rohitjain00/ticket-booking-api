from datetime import datetime

from app.main.model.ticket import Ticket
from app.main.util.date_time_format import strp_date, strp_time
from app.main.util.db import delete_database_entry, save_database_change

from .movie_service import is_valid_movie
from .show_time_service import get_time, is_valid_time
from .user_service import get_user_from_id, get_user_id

max_tickets = 20


def book_a_ticket(data):
    """Gets the data for booking a ticket"""
    movie_id = data['movie_id']
    date = data['date']
    time_id = data['time_id']
    name = data['name']
    number = data['number']

    if not is_valid_movie(movie_id) or not is_valid_time(time_id):
        return {
            "status": "Fail",
            "Message": "Invalid movie_id or time_id"
        }, 401

    user_id = get_user_id(name, number)
    s_time = strp_time(get_time(time_id).time)
    s_date = strp_date(date)

    if are_all_seats_booked(movie_id, date, time_id):
        return {
            "status": "Fail",
            "Message": "All the 20 seats are booked for this time."
        }, 401
    curr_datetime = datetime.now()
    movie_datetime = datetime.combine(s_date, s_time.time())
    if curr_datetime > movie_datetime:
        return {
            "status": "Fail",
            "Message": "Please book a ticket for a future time"
        }, 401

    new_ticket = Ticket(date=date, is_expired=False, movie=movie_id, show_time_id=time_id, user_id=user_id)
    save_database_change(new_ticket)
    return {
        "status": "Pass",
        "Message": "Ticket booked successfully",
        "ticket_id": new_ticket.id
    }, 201


def update_ticket_time(ticket_id, time_id):
    ticket = Ticket.query.filter_by(id=ticket_id).first()
    ticket.show_time_id = time_id
    save_database_change(ticket)


def update_a_ticket(data):
    """Gets data to update the user's ticket"""
    ticket_id = data['ticket_id']
    time_id = data['time_id']
    number = data['number']
    if not is_valid_ticket(ticket_id) or not is_valid_time(time_id):
        return {
            "status": "Fail",
            "message": "ticket id or time id is not valid"
        }, 401
    if not matches_ticket_number(ticket_id, number):
        return {
            "status": "Fail",
            "message": "number does not matches the ticket"
        }, 401

    update_ticket_time(ticket_id, time_id)
    return {
        "status": "Pass",
        "message": "Time updated successfully"
    }, 201


def tickets_with_date_time(data):
    movie_id = data.get('movie_id')
    time_id = data.get('time_id')
    date = data.get('date')
    tickets = Ticket.query.filter_by(movie=movie_id, show_time_id=time_id, date=date).all()
    return tickets


def delete_ticket_db(ticket_id):
    ticket = Ticket.query.filter_by(id=ticket_id).first()
    delete_database_entry(ticket)


def delete_a_ticket(data):
    ticket_id = data['ticket_id']
    time_id = data['time_id']
    number = data['number']
    if not is_valid_ticket(ticket_id) or not is_valid_time(time_id):
        return {
                   "status": "Fail",
                   "message": "ticket id or time id is not valid"
               }, 401
    if not matches_ticket_number(ticket_id, number):
        return {
                   "status": "Fail",
                   "message": "number does not matches the ticket"
               }, 401

    delete_ticket_db(ticket_id)
    return {
               "status": "Pass",
               "message": "Ticket Deleted Successfully"
           }, 201


def user_details_from_ticket_id(ticket_id):
    if not is_valid_ticket(ticket_id):
        return {
            "status": "Fail",
            "message": "ticket id is not valid"
        }, 401

    ticket = Ticket.query.filter_by(id=ticket_id).first()
    user = get_user_from_id(ticket.user_id)
    return user, 201


def are_all_seats_booked(movie_id, date, time_id):
    """
    :param movie_id:
    :param date:
    :param time:
    :return: checks if the movie has all the seats booked
    """
    return Ticket.query.filter_by(movie=movie_id, date=date, show_time_id=time_id).count() >= max_tickets


def is_valid_ticket(ticket_id):
    return Ticket.query.filter_by(id=ticket_id).count() == 1


def matches_ticket_number(ticket_id, number):
    ticket = Ticket.query.filter_by(id=ticket_id).first()
    return get_user_from_id(ticket.user_id).number == number
