from datetime import timedelta


def to_microseconds(td):
    if isinstance(td, timedelta):
        return td.days * 86400000000 + td.seconds * 1000000 + td.microseconds
