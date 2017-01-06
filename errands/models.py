from __future__ import unicode_literals

from django.db import models
from datetime import datetime as dt, timedelta as td
import json


class Std:
    std_d_format = '%d/%m/%Y'
    input_d_format = '%Y-%m-%d'
    output_d_format = '%Y-%m-%d'

    std_t_format = '%H:%M:%S'
    input_t_format = '%H:%M'
    output_t_format = '%H:%M'

    input_dt_format = '%Y-%m-%d %H:%M'
    output_dt_format = '%Y-%m-%d %H:%M'

    user_identity = 'panduscientist'

    class Keys:
        pk = 'pk'
        time_period = 'time_period'
        epoch_date = 'epoch_date'
        epoch_time = 'epoch_time'
        duration = 'duration'

        tag = 'tag'
        comment = 'comment'

        days = 'days'
        seconds = 'seconds'

        user_logged_in = 'user_logged_in'

        def __init__(self):
            pass

    def __init__(self):
        pass


class Errand(models.Model):
    description = models.TextField(blank=True)

    def __init__(self, *args, **kwargs):
        super(Errand, self).__init__(*args, **kwargs)
        self.deserialize()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        if self.serialize() is not False:
            super(Errand, self).save(force_insert=force_insert, force_update=force_update, using=using,
                                     update_fields=update_fields)

    def set(self, tag, comment, misc):
        self.tag = tag
        self.comment = comment
        self.misc = misc

    def deserialize(self):
        """
        :return: True if all extraction is done
                 False otherwise
        """
        try:
            json_obj = json.loads(self.description)
            # tag
            self.tag = json_obj[Std.Keys.tag]
            del json_obj[Std.Keys.tag]
            # comment
            self.comment = json_obj[Std.Keys.comment]
            del json_obj[Std.Keys.comment]
            # miscellaneous
            self.misc = {}
            for arg in json_obj:
                self.misc[arg] = json_obj[arg]

        except ValueError:
            return False
        except KeyError:
            return False
        except AttributeError:
            return False

        return True

    def serialize(self):
        """
        :return: the serialized value
                 False if error occurs
        """
        try:
            description = {
                # tag
                Std.Keys.tag: self.tag,
                # comment
                Std.Keys.comment: self.comment,
            }
            # misc
            for key in self.misc:
                description[key] = self.misc[key]

            self.description = json.dumps(description)

        except AttributeError:
            return False

        return self.description

    def __str__(self):
        return self.description


class Piece(models.Model):
    """
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

    def __init__(self, *args, **kwargs):
        super(Piece, self).__init__(*args, **kwargs)
        self.deserialize()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        if self.serialize() is not False:
            super(Piece, self).save(force_insert=force_insert, force_update=force_update, using=using,
                                    update_fields=update_fields)

    def set(self, tag, comment, misc, epoch_date, epoch_time, time_period, duration):
        self.tag = tag
        self.comment = comment
        self.misc = misc
        self.epoch_time = epoch_time
        self.epoch_date = epoch_date
        self.time_period = time_period
        self.duration = duration

    def deserialize(self):
        """
        :return: True if all extraction is done
                 False otherwise
        """
        try:
            json_obj = json.loads(self.description)
            # tag
            self.tag = json_obj[Std.Keys.tag]
            del json_obj[Std.Keys.tag]
            # comment
            self.comment = json_obj[Std.Keys.comment]
            del json_obj[Std.Keys.comment]
            # time_period
            j_time_period = json_obj[Std.Keys.time_period]
            del json_obj[Std.Keys.time_period]
            self.time_period = td(days=j_time_period[Std.Keys.days], seconds=j_time_period[Std.Keys.seconds])
            # duration
            j_duration = json_obj[Std.Keys.duration]
            del json_obj[Std.Keys.duration]
            self.duration = td(days=j_duration[Std.Keys.days], seconds=j_duration[Std.Keys.seconds])
            # epoch time
            self.epoch_time = dt.strptime(json_obj[Std.Keys.epoch_time], Std.std_t_format).time()
            del json_obj[Std.Keys.epoch_time]
            # epoch date
            self.epoch_date = dt.strptime(json_obj[Std.Keys.epoch_date], Std.std_d_format).date()
            del json_obj[Std.Keys.epoch_date]
            # miscellaneous
            self.misc = {}
            for arg in json_obj:
                self.misc[arg] = json_obj[arg]
        except ValueError:
            return False
        except KeyError:
            return False
        except AttributeError:
            return False

        return True

    def serialize(self):
        """
        :return: the serialized value
                 False if error occurs
        """
        try:
            description = {
                # tag
                Std.Keys.tag: self.tag,
                # comment
                Std.Keys.comment: self.comment,
                # epoch_date
                Std.Keys.epoch_date: self.epoch_date.strftime(Std.std_d_format),
                # epoch_date
                Std.Keys.epoch_time: self.epoch_time.strftime(Std.std_t_format),
                # time_period
                Std.Keys.time_period: {
                    Std.Keys.days: self.time_period.days,
                    Std.Keys.seconds: self.time_period.seconds,
                },
                # duration
                Std.Keys.duration: {
                    Std.Keys.days: self.duration.days,
                    Std.Keys.seconds: self.duration.seconds,
                },
            }
            # misc
            for key in self.misc:
                description[key] = self.misc[key]

            self.description = json.dumps(description)
        except AttributeError:
            return False

        return self.description

    def __str__(self):
        return self.description
