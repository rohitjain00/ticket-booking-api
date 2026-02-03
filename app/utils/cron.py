from datetime import datetime

from app.models.ticket import Ticket
from app.services.show_time_service import get_time
from app.utils.date_time_format import strp_date, strp_time
from app.extensions import db


def set_ticket_expired():
    tickets = Ticket.query.all()
    for ticket in tickets:
        time_id = ticket.show_time_id
        date = ticket.date
        s_time = strp_time(get_time(time_id).time)
        s_date = strp_date(date)
        curr_datetime = datetime.now()
        movie_datetime = datetime.combine(s_date, s_time.time())

        diff = curr_datetime - movie_datetime
        days, seconds = diff.days, diff.seconds
        hours = days * 24 + seconds // 3600
        if hours >= 8:
            ticket.is_expired = True
    db.session.commit()


def delete_expired_ticket():
    tickets = Ticket.query.all()
    for ticket in tickets:
        if ticket.is_expired:
            db.session.delete(ticket)
    db.session.commit()
