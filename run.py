import os
from app import create_app, db

from app.models.ticket import Ticket
from app.models.user import User
from app.models.movie import Movie
from app.models.show_time import ShowTime
from app.utils.seed import push_initial_data

app = create_app(os.getenv('FLASK_CONFIG', 'dev'))

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Ticket=Ticket, User=User, Movie=Movie, ShowTime=ShowTime)

@app.cli.command("seed")
def seed():
    """Seed the database with initial data."""
    push_initial_data()
    print("Database seeded!")
