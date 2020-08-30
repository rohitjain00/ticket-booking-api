from app.main.model.movie import Movie
from app.main.model.show_time import ShowTime
from app.main import db


def push_initial_data():
    show_time = ShowTime.query.first()
    if show_time is None:
        show_time = ShowTime(time="15:00")
        db.session.add(show_time)

    movie = Movie.query.first()
    if movie is None:
        movie = Movie(name='3 Idiots', start_date='25-08-2020', end_date='25-09-2020', show_time=[show_time])
        db.session.add(movie)
    else:
        movie = Movie.query.first()

    db.session.commit()
