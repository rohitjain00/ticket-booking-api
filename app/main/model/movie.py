from .. import db

movie_show_time = db.Table('movie_show_time',
                           db.Column("movie_id", db.Integer, db.ForeignKey('movie.id'), primary_key=True),
                           db.Column("show_time_id", db.Integer, db.ForeignKey('show_time.id'), primary_key=True)
                           )


class Movie(db.Model):
    """ Model for storing different movies"""

    __tablename__ = "movie"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    start_date = db.Column(db.String(20))
    end_date = db.Column(db.String(20))
    show_time = db.relationship('ShowTime', secondary=movie_show_time, lazy='subquery',
                                backref=db.backref('movie', lazy=True))

    def __repr__(self):
        return "<User '{}' '{}'>".format(self.name, self.number)
