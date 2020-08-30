from app.main.model.show_time import ShowTime


def get_time(time_id):
    return ShowTime.query.filter_by(id=time_id).first()


def is_valid_time(time_id):
    return True
