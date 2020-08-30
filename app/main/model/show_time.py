from .. import db


class ShowTime(db.Model):
    """ Show Time model for storing different time for movie"""

    __tablename__ = "show_time"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time = db.Column(db.String(50))

    def __repr__(self):
        return "<ShowTime '{}'>".format(self.time)

