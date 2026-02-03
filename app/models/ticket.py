from app.extensions import db


class Ticket(db.Model):
    """ Ticket model for storing user's Ticket'"""

    __tablename__ = "ticket"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.String(50))
    is_expired = db.Column(db.Boolean, default=False)
    movie = db.Column(db.Integer, db.ForeignKey('movie.id'))
    show_time_id = db.Column(db.Integer, db.ForeignKey('show_time.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return "<Ticket '{}' '{}' '{}' '{}' '{}'>".format(self.id, self.user_id, self.movie, self.show_time_id, self.user_id)
