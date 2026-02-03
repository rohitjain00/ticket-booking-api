from app.extensions import db


def save_database_change(data):
    db.session.add(data)
    db.session.commit()


def delete_database_entry(data):
    db.session.delete(data)
    db.session.commit()
