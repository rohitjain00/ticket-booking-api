from flask_restplus import Namespace, fields


class UserDto:
    api = Namespace("user", description="User Model")
    user = api.model(
        "user",
        {
            # "id": fields.Integer(
            #     required=True, description="user's id"
            # ),
            "name": fields.String(
                required=True, description="user's name"
            ),
            "number": fields.String(
                required=True, description="user's number"
            )
        }
    )


class ShowTimeDto:
    api = Namespace('showtime', description="store the different timing of the shows")
    show_time = api.model(
        "show_time",
        {
            # "id": fields.Integer(
            #     required=True, description="show time's id"
            # ),
            "time": fields.String(
                required=True, description="time of the day for the show"
            )
        }
    )


class MovieDto:
    api = Namespace('movie', description="Movie's model")
    movie = api.model(
        "ticket",
        {
            # "id": fields.Integer(
            #     required=True, description="movie's id"
            # ),
            "name": fields.String(
                required=True, description="movie's name"
            ),
            "start_date": fields.String(
                required=True, description="movie's start date"
            ),
            "end_date": fields.String(
                required=True, description="movie's end date"
            ),
            "show_time": fields.List(fields.Nested(ShowTimeDto.show_time))
        }
    )


class TicketDto:
    api = Namespace('ticket', description="Ticket Model")
    ticket = api.model(
        "ticket",
        {
            "id": fields.Integer(
                required=True, description="ticket's id"
            ),
            "movie_id": fields.Integer(
                required=True, description="ticket's movie id"
            ),
            "date": fields.String(
                required=True, description="movie's date"
            ),
            "time_id": fields.Integer(
                required=True, description="ticket's time id"
            ),
        }
    )
    ticket_book = api.model(
        "ticket_book",
        {
            "movie_id": fields.Integer(
                required=True, description="Movie's id"
            ),
            "date": fields.String(
                required=True, description="movie's date"
            ),
            "time_id": fields.Integer(
                required=True, description="Show time's Id"
            ),
            "name": fields.String(
                required=True, description="user's name"
            ),
            "number": fields.String(
                required=True, description="User's number"
            ),
        }
    )
    ticket_update = api.model(
        "ticket_update",
        {
            "ticket_id": fields.Integer(
                required=True, description="ticket's id"
            ),
            "time_id": fields.Integer(
                required=True, description="Show time's Id"
            ),
            "number": fields.String(
                required=True, description="User's number"
            ),
        }
    )
