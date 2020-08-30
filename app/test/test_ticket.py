import datetime
import json
import unittest
from urllib import parse

from app.main.model.movie import Movie
from app.main.model.show_time import ShowTime
from app.main.model.user import User
from app.main.util.db import save_database_change
from app.test.base import BaseTestCase

future_date = '05-09-2020'
past_date = '25-08-2020'


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


def book_ticket(self, movie_id, date, time_id, name, number):
    return self.client.post(
        "/ticket/",
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


class TestTicketBook(BaseTestCase):

    def test_book_ticket(self):
        with self.client:
            user = create_user()
            time = create_time()
            movie = create_movie(time)

            response = book_ticket(self, movie_id=movie.id, date=future_date, time_id=time.id, name=user.name, number=user.number)
            response_json = response.json
            self.assertEqual(response_json['status'], 'Pass')
            self.assertEqual(response_json['Message'], 'Ticket booked successfully')
            self.assertEqual(response_json['ticket_id'], 1)
            self.assertEqual(response.status_code, 201)

    def test_book_past_ticket(self):
        with self.client:
            user = create_user()
            time = create_time()
            movie = create_movie(time)

            response = book_ticket(self, movie_id=movie.id, date=past_date, time_id=time.id, name=user.name, number=user.number)
            response_json = response.json
            self.assertEqual(response_json['status'], 'Fail')
            self.assertEqual(response_json['Message'], 'Please book a ticket for a future time')
            self.assertEqual(response.status_code, 401)

    def test_book_21_tickets(self):
        with self.client:
            user = create_user()
            time = create_time()
            movie = create_movie(time)
            for i in range(0, 20):
                response = book_ticket(self, movie_id=movie.id, date=future_date, time_id=time.id, name=user.name, number=user.number)
                self.assertEqual(response.status_code, 201)
            response = book_ticket(self, movie_id=movie.id, date=future_date, time_id=time.id, name=user.name,
                                   number=user.number)
            response_json = response.json
            self.assertEqual(response_json['status'], 'Fail')
            self.assertEqual(response_json['Message'], 'All the 20 seats are booked for this time.')
            self.assertEqual(response.status_code, 401)

    def test_book_ticket_multiple_user(self):
        with self.client:
            user = create_user()
            time = create_time()
            movie = create_movie(time)

            response = book_ticket(self, movie_id=movie.id, date=future_date, time_id=time.id, name=user.name,
                                   number=user.number)
            total_user = User.query.count()
            self.assertEqual(total_user, 1)
            response = book_ticket(self, movie_id=movie.id, date=future_date, time_id=time.id, name='Test2',
                                   number='8888888888')
            total_user = User.query.count()
            self.assertEqual(total_user, 2)
            response = book_ticket(self, movie_id=movie.id, date=future_date, time_id=time.id, name='Test3',
                                   number='7777777777')
            total_user = User.query.count()
            self.assertEqual(total_user, 3)


def update_ticket(self, ticket_id, time_id, number):
    return self.client.put(
        "/ticket/",
        data=json.dumps(
            dict(
                ticket_id=ticket_id,
                time_id=time_id,
                number=number
            )
        )
    )


def create_another_time(time):
    t = ShowTime(time=time)
    save_database_change(t)
    return t


class TestTicketUpdate(BaseTestCase):

    def test_ticket_update(self):
        with self.client:
            user = create_user()
            time = create_time()
            time2 = create_another_time('23:50')
            movie = create_movie(time)

            response = book_ticket(self, movie_id=movie.id, date=future_date, time_id=time.id, name=user.name,
                                   number=user.number)
            ticket_id = response.json['ticket_id']

            response = update_ticket(self, ticket_id, time2.id, user.number)
            response_json = response.json
            self.assertEqual(response_json['status'], 'Pass')
            self.assertEqual(response_json['message'], 'Time updated successfully')
            self.assertEqual(response.status_code, 201)


def delete_ticket(self, ticket_id, time_id, number):
    return self.client.delete(
        "/ticket/",
        data=json.dumps(
            dict(
                ticket_id=ticket_id,
                time_id=time_id,
                number=number
            )
        ),
        content_type="application/json"
    )


class TestTicketDelete(BaseTestCase):
    def test_ticket_delete(self):
        with self.client:
            user = create_user()
            time = create_time()
            movie = create_movie(time)

            response = book_ticket(self, movie_id=movie.id, date=future_date, time_id=time.id, name=user.name,
                                   number=user.number)
            ticket_id = response.json['ticket_id']
            response = delete_ticket(self, ticket_id, time.id, user.number)
            response_json = response.json
            self.assertEqual(response_json['status'], 'Pass')
            self.assertEqual(response_json['message'], 'Ticket Deleted Successfully')
            self.assertEqual(response.status_code, 201)


def user_details_from_ticket(self, ticket_id):
    return self.client.get('/ticket/u/'+str(ticket_id), content_type="application/json")


class TestUserDetailsFromTicket(BaseTestCase):
    def test_user_details_ticket_id(self):
        with self.client:
            user = create_user()
            time = create_time()
            movie = create_movie(time)

            response = book_ticket(self, movie_id=movie.id, date=future_date, time_id=time.id, name=user.name,
                                   number=user.number)
            ticket_id = response.json['ticket_id']
            response = user_details_from_ticket(self, ticket_id)
            response_json = response.json
            self.assertTrue(response_json['user'])
            self.assertEqual(response_json['user']['name'], 'Test')
            self.assertEqual(response_json['user']['number'], '9999999999')
            self.assertEqual(response.status_code, 201)


def test_ticket_particular_time(self, movie_id, date, time_id):
    p = {
            'movie_id': movie_id,
            'date': date,
            'time_id': time_id
        }
    return self.client.get(
        "/ticket/?"+parse.urlencode(p)
    )


class TestAllTicketsWithParticularTime(BaseTestCase):
    def test_tickets_with_particular_time(self):
        with self.client:
            time = create_time()
            movie = create_movie(time)

            for i in range(0, 10):
                book_ticket(self, movie_id=movie.id, date=future_date, time_id=time.id, name='Test2', number='8888888888')
            response = test_ticket_particular_time(self, movie_id=movie.id, date=future_date, time_id=time.id)
            response_json = response.json
            self.assertEqual(len(response_json['tickets']), 10)
