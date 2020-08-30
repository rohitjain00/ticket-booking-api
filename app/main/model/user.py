from .. import db


class User(db.Model):
    """ User model for storing user details"""

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    number = db.Column(db.String(15), unique=True)

    def __repr__(self):
        return "<User '{}' '{}'>".format(self.name, self.number)
