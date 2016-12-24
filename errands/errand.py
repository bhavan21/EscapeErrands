import json
from datetime import datetime as dt, timedelta as td


class JKeys:
    time_period = 'time_period'
    epoch_date = 'epoch_date'
    epoch_time = 'epoch_time'
    duration = 'duration'

    days = 'days'
    hours = 'hours'
    minutes = 'minutes'
    seconds = 'seconds'

    pieces = 'pieces'
    additional = 'additional'

    def __init__(self):
        pass


class Piece:
    """
     assumptions
     time_period (generally integral number of days)
        == 0 : no-repeat
        >  0 : repeat

     duration
        == 0 : point (task)
        >  0 : line (event)

     for repeating pieces
        epoch_date must be the day first time the piece would start
        epoch_time is (obviously) the time in day where the piece would start after every time period
     """

    std_d_format = '%d/%m/%Y'
    std_t_format = '%H:%M:%S'
    std_dt_format = '%d/%m/%Y %H:%M:%S'

    def __init__(self, dict_info=None):
        """
        initialization using a dictionary
        """
        if dict_info is not None:
            """
            assumes that all critical key-value pairs are present in 'dict_info'
            the other parameters are ignored
            self.misc is None
            """
            self.dict_info = dict_info
            # time_period
            j_time_period = dict_info[JKeys.time_period]
            self.time_period = td(days=j_time_period[JKeys.days], seconds=j_time_period[JKeys.seconds])
            # duration
            j_duration = dict_info[JKeys.duration]
            self.duration = td(days=j_duration[JKeys.days], seconds=j_duration[JKeys.seconds])
            # epoch time
            self.epoch_time = dt.strptime(dict_info[JKeys.epoch_time], Piece.std_t_format).time()
            # epoch date
            self.epoch_date = dt.strptime(dict_info[JKeys.epoch_date], Piece.std_d_format).date()
            self.kwargs = {}
            for arg in dict_info:
                if arg != JKeys.time_period \
                        and arg != JKeys.duration \
                        and arg != JKeys.epoch_date \
                        and arg != JKeys.epoch_time:
                    self.kwargs[arg] = dict_info[arg]

        else:
            """
            no dict_info
            """
            self.time_period = None
            self.duration = None
            self.epoch_date = None
            self.epoch_time = None
            self.kwargs = None

    def serialize(self):
        params_dict = {
            JKeys.epoch_time: self.epoch_time.strftime(Piece.std_t_format),
            JKeys.epoch_date: self.epoch_date.strftime(Piece.std_d_format),
            JKeys.time_period: {
                JKeys.days: self.time_period.days,
                JKeys.seconds: self.time_period.seconds
            },
            JKeys.duration: {
                JKeys.days: self.duration.days,
                JKeys.seconds: self.duration.seconds
            }
        }
        for arg in self.kwargs:
            params_dict[arg] = self.kwargs[arg]

        return json.dumps(params_dict)

    def belongs_to(self, date_param):
        """
        :param date_param
        :return
        if belongs self
        otherwise False
        """
        if self.time_period.days == 0 and self.time_period.seconds == 0:
            # Non-Repeating
            epoch = dt.combine(self.epoch_date, self.epoch_time)
            end = epoch + self.duration
            if epoch.date() == date_param or end.date() == date_param:
                return self
            else:
                return False

        elif self.time_period.days > 0 or self.time_period.seconds > 0:
            # Repeating
            epoch = dt.combine(self.epoch_date, self.epoch_time)
            now = dt.now()
            delta = now - epoch

            """
            this (delta.days % self.time_period.days == 0)
            setting makes sure to return true if any portion of the piece belongs to the given param
            """
            # epoch
            if delta.days % self.time_period.days == 0:
                # this piece occurs on date_param
                return self

            # end
            end = epoch + self.duration
            delta = now - end
            if delta.days % self.time_period.days == 0:
                # this piece occurs on date_param
                return self

            return False

    def __repr__(self):
        about = ''
        if self.time_period is not None:
            if self.time_period.days == 0 and self.time_period.seconds == 0:
                about += 'Non-Repeating'
            else:
                about += 'Repeating'

        if self.duration is not None:
            if self.duration.days == 0 and self.duration.seconds == 0:
                about += ' Task'
            else:
                about += ' Event'

        about += ' Piece'

        return about


class Errand:
    """
    Ordered List of pieces and some details makes an errand
    """

    def __init__(self, list_info=None, additional=None):
        """
        :param list_info: list of dictionaries for making pieces
        :param additional: dict for other decoration
        """
        self.pieces = []
        self.additional = additional
        if list_info is not None:
            """
            assumes that list of pieces is valid
            """
            for piece in list_info:
                self.pieces.append(Piece(piece))

    def serialize(self):
        list_of_pieces = []
        for piece in self.pieces:
            list_of_pieces.append(piece.serialize())
        total = {JKeys.pieces: list_of_pieces, JKeys.additional: self.additional}
        return json.dumps(total)

    def subset_in(self, date_param):
        """
        :param date_param: 
        :return list of pieces in json_string form which occur in the given date_param 
        if zero of its pieces belongs to the day returns False 
        """
        set_of_indices = []
        count = 0
        for piece in self.pieces:
            ret = piece.belongs_to(date_param)
            if ret is not False:
                set_of_indices.append(count)
            count += 1

        if len(set_of_indices) == 0:
            return False
        else:
            return set(set_of_indices)


s1 = {
    "time_period": {"days": 7, "seconds": 0},
    "duration": {"days": 0, "seconds": 0},
    "epoch_time": "10:14:00",
    "epoch_date": "10/12/2014"
}

s2 = {
    "time_period": {"days": 7, "seconds": 0},
    "duration": {"days": 0, "seconds": 0},
    "epoch_time": "10:14:00",
    "epoch_date": "3/12/2014"
}

s3 = {
    "tag": "hello",
    "time_period": {"days": 7, "seconds": 0},
    "duration": {"days": 0, "seconds": 0},
    "epoch_time": "10:14:00",
    "epoch_date": "17/12/2014",
    "next": 1,
    "prev": 2
}

'{"tag": "hello","time_period": {"days": 7, "seconds": 0},"duration": {"days": 0, "seconds": 0},"epoch_time": "10:14:00","epoch_date": "17/12/2014","next": 1,"prev": 2}'

a1 = Piece(dict_info=s1)
a2 = Piece(dict_info=s2)
b = Errand([s1, s2])
c = Errand([s1, s2, s3])
