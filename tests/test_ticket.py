import json
import pytest
import datetime
from urllib import parse

from app.models.movie import Movie
from app.models.show_time import ShowTime
from app.models.user import User
from app.utils.db import save_database_change

today = datetime.date.today()
future_date = (today + datetime.timedelta(days=10)).strftime('%d-%m-%Y')
past_date = (today - datetime.timedelta(days=10)).strftime('%d-%m-%Y')

def create_user():
    user = User(name='Test', number='9999999999')
    save_database_change(user)
    return user

def create_movie(time):
    movie = Movie(name='ASDF', start_date='20-08-2020', end_date='25-09-2020', show_time=[time])
    save_database_change(movie)
    return movie

def create_time():
    time = ShowTime(time='23:59')
    save_database_change(time)
    return time

def book_ticket(client, movie_id, date, time_id, name, number):
    return client.post(
        "/api/ticket/",
        data=json.dumps(
            dict(
                movie_id=movie_id,
                date=date,
                time_id=time_id,
                name=name,
                number=number
            )
        ),
        content_type="application/json",
    )

def test_book_ticket(client, db):
    user = create_user()
    time = create_time()
    movie = create_movie(time)

    response = book_ticket(client, movie_id=movie.id, date=future_date, time_id=time.id, name=user.name, number=user.number)
    response_json = response.json
    assert response.status_code == 201
    assert response_json['status'] == 'Pass'
    assert response_json['Message'] == 'Ticket booked successfully'
    assert response_json['ticket_id'] == 1

def test_book_past_ticket(client, db):
    user = create_user()
    time = create_time()
    movie = create_movie(time)

    response = book_ticket(client, movie_id=movie.id, date=past_date, time_id=time.id, name=user.name, number=user.number)
    response_json = response.json
    assert response.status_code == 401
    assert response_json['status'] == 'Fail'
    assert response_json['Message'] == 'Please book a ticket for a future time'

def test_book_21_tickets(client, db):
    user = create_user()
    time = create_time()
    movie = create_movie(time)
    for i in range(0, 20):
        response = book_ticket(client, movie_id=movie.id, date=future_date, time_id=time.id, name=user.name, number=user.number)
        assert response.status_code == 201

    # 21st ticket
    response = book_ticket(client, movie_id=movie.id, date=future_date, time_id=time.id, name=user.name, number=user.number)
    response_json = response.json
    assert response.status_code == 401
    assert response_json['status'] == 'Fail'
    assert response_json['Message'] == 'All the 20 seats are booked for this time.'

def test_book_ticket_multiple_user(client, db):
    user = create_user()
    time = create_time()
    movie = create_movie(time)

    book_ticket(client, movie_id=movie.id, date=future_date, time_id=time.id, name=user.name, number=user.number)
    assert User.query.count() == 1

    book_ticket(client, movie_id=movie.id, date=future_date, time_id=time.id, name='Test2', number='8888888888')
    assert User.query.count() == 2

    book_ticket(client, movie_id=movie.id, date=future_date, time_id=time.id, name='Test3', number='7777777777')
    assert User.query.count() == 3

def update_ticket(client, ticket_id, time_id, number):
    return client.put(
        "/api/ticket/",
        data=json.dumps(
            dict(
                ticket_id=ticket_id,
                time_id=time_id,
                number=number
            )
        ),
        content_type="application/json"
    )

def create_another_time(time):
    t = ShowTime(time=time)
    save_database_change(t)
    return t

def test_ticket_update(client, db):
    user = create_user()
    time = create_time()
    time2 = create_another_time('23:50')
    movie = create_movie(time)

    response = book_ticket(client, movie_id=movie.id, date=future_date, time_id=time.id, name=user.name, number=user.number)
    ticket_id = response.json['ticket_id']

    response = update_ticket(client, ticket_id, time2.id, user.number)
    response_json = response.json
    assert response.status_code == 201
    assert response_json['status'] == 'Pass'
    assert response_json['message'] == 'Time updated successfully'

def delete_ticket(client, ticket_id, time_id, number):
    return client.delete(
        "/api/ticket/",
        data=json.dumps(
            dict(
                ticket_id=ticket_id,
                time_id=time_id,
                number=number
            )
        ),
        content_type="application/json"
    )

def test_ticket_delete(client, db):
    user = create_user()
    time = create_time()
    movie = create_movie(time)

    response = book_ticket(client, movie_id=movie.id, date=future_date, time_id=time.id, name=user.name, number=user.number)
    ticket_id = response.json['ticket_id']

    response = delete_ticket(client, ticket_id, time.id, user.number)
    response_json = response.json
    assert response.status_code == 201
    assert response_json['status'] == 'Pass'
    assert response_json['message'] == 'Ticket Deleted Successfully'

def user_details_from_ticket(client, ticket_id):
    return client.get('/api/ticket/u/'+str(ticket_id), content_type="application/json")

def test_user_details_ticket_id(client, db):
    user = create_user()
    time = create_time()
    movie = create_movie(time)

    response = book_ticket(client, movie_id=movie.id, date=future_date, time_id=time.id, name=user.name, number=user.number)
    ticket_id = response.json['ticket_id']

    response = user_details_from_ticket(client, ticket_id)
    response_json = response.json
    assert response.status_code == 201
    assert response_json['user']['name'] == 'Test'
    assert response_json['user']['number'] == '9999999999'

def call_test_ticket_particular_time(client, movie_id, date, time_id):
    p = {
            'movie_id': movie_id,
            'date': date,
            'time_id': time_id
        }
    return client.get(
        "/api/ticket/?"+parse.urlencode(p)
    )

def test_tickets_with_particular_time(client, db):
    time = create_time()
    movie = create_movie(time)

    for i in range(0, 10):
        book_ticket(client, movie_id=movie.id, date=future_date, time_id=time.id, name='Test2', number='8888888888')

    response = call_test_ticket_particular_time(client, movie_id=movie.id, date=future_date, time_id=time.id)
    response_json = response.json
    assert len(response_json['tickets']) == 10
