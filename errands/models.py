from __future__ import unicode_literals

from django.db import models
from datetime import datetime as dt, timedelta as td
import json


class Std:
    std_d_format = '%d/%m/%Y'
    std_t_format = '%H:%M:%S'
    std_dt_format = '%d/%m/%Y %H:%M:%S'

    class JKeys:
        time_period = 'time_period'
        epoch_date = 'epoch_date'
        epoch_time = 'epoch_time'
        duration = 'duration'

        tag = 'tag'
        comment = 'comment'

        days = 'days'
        seconds = 'seconds'

        def __init__(self):
            pass

    def __init__(self):
        pass


class Errand(models.Model):
    description = models.TextField(blank=True)

    def deserialize(self):
        json_obj = json.loads(self.description)
        # tag
        self.tag = json_obj[Std.JKeys.tag]
        del json_obj[Std.JKeys.tag]
        # comment
        self.comment = json_obj[Std.JKeys.comment]
        del json_obj[Std.JKeys.tag]
        # miscellaneous
        self.misc = {}
        for arg in json_obj:
            self.misc[arg] = json_obj[arg]

        return json_obj

    def __str__(self):
        return self.description


class Piece(models.Model):
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
    description = models.TextField(blank=True)
    errand = models.ForeignKey(Errand, on_delete=models.CASCADE, null=True)

    def deserialize(self):
        """
        assumes the description contains the below extracted tags
        :return: json object of self.description
        """
        json_obj = json.loads(self.description)
        # tag
        self.tag = json_obj[Std.JKeys.tag]
        del json_obj[Std.JKeys.tag]
        # comment
        self.comment = json_obj[Std.JKeys.comment]
        del json_obj[Std.JKeys.tag]
        # time_period
        j_time_period = json_obj[Std.JKeys.time_period]
        del json_obj[Std.JKeys.time_period]
        self.time_period = td(days=j_time_period[Std.JKeys.days], seconds=j_time_period[Std.JKeys.seconds])
        # duration
        j_duration = json_obj[Std.JKeys.duration]
        del json_obj[Std.JKeys.duration]
        self.duration = td(days=j_duration[Std.JKeys.days], seconds=j_duration[Std.JKeys.seconds])
        # epoch time
        self.epoch_time = dt.strptime(json_obj[Std.JKeys.epoch_time], Std.std_t_format).time()
        del json_obj[Std.JKeys.epoch_time]
        # epoch date
        self.epoch_date = dt.strptime(json_obj[Std.JKeys.epoch_date], Std.std_d_format).date()
        del json_obj[Std.JKeys.epoch_date]
        # miscellaneous
        self.misc = {}
        for arg in json_obj:
            self.misc[arg] = json_obj[arg]

        return json_obj

    def __str__(self):
        return self.description
