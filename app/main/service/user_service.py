from app.main.model.user import User
from app.main.util.db import save_database_change


def get_user_id(name, number):
    """
    Returns/Creates the User associated with the name and number.
    :param name: Name of the user
    :param number: Number of the user
    :return: Return the User object.
    """
    user = User.query.filter_by(name=name, number=number).first()
    if user is None:
        new_user = User(name=name, number=number)
        save_database_change(new_user)
        return new_user.id
    else:
        return user.id


def get_user_from_id(user_id):
    return User.query.filter_by(id=user_id).first()

