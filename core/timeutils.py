from datetime import datetime as dt, timedelta as td


def to_microseconds(time_delta):
    if isinstance(time_delta, time_delta):
        return time_delta.days * 86400000000 + time_delta.seconds * 1000000 + time_delta.microseconds


class Stub:
    def __init__(self, epoch=dt.now(), end=dt.now(), duration=td()):
        self.epoch = epoch
        self.end = end
        self.duration = duration

    def is_valid(self):
        if self.epoch is not None and isinstance(self.epoch, dt) \
                and self.end is not None and isinstance(self.end, dt) \
                and self.duration is not None and isinstance(self.duration, td) and self.duration > td() \
                and self.epoch + self.duration == self.end:
            return True
        else:
            return False

    def __str__(self):
        return str((self.epoch, self.end))

    def __hash__(self):
        return hash((self.epoch, self.end, self.duration))

    def __eq__(self, other):
        return (self.epoch, self.end, self.duration) == (other.epoch, other.end, other.duration)
