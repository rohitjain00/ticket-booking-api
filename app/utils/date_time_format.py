import datetime

# date in format 31-06-2020
date_format = '%d-%m-%Y'
time_format = '%H:%M'


def strp_date(date):
    """
    Converts the date
    :param date:
    :return:
    """
    return datetime.datetime.strptime(date, date_format)


def strp_time(time):
    """
    Converts the time
    :param time:
    :return:
    """
    return datetime.datetime.strptime(time, time_format)
