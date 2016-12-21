from datetime import datetime


def get_datetime(day, month, year, hour, minute, second):
    return datetime(day=day, month=month, year=year, hour=hour, minute=minute, second=second)


def to_string(instance, form):
    instance.strftime(format=form)
