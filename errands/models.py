from __future__ import unicode_literals

from django.db import models
from datetime import datetime as dt, timedelta as td
from time_table.colors import color_map
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

    class Keys:
        pk = 'pk'
        time_period = 'time_period'
        epoch_date = 'epoch_date'
        epoch_time = 'epoch_time'
        end_date = 'end_date'
        end_time = 'end_time'
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

     end (Limiting datetime for a piece)
        Piece cannot have stubs which epoch after end (if end is specified).

        Assumption: while initializing end_date and end_time either both are complete and valid
                                                                or both are empty strings

        Non-repeating pieces: Always both empty strings
        Repeating pieces:     Both empty strings (never ending)
                            Or Both fully filled

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

    def set(self, tag, comment, misc, epoch_date, epoch_time, end_date, end_time, time_period, duration):
        self.tag = tag
        self.comment = comment
        self.misc = misc
        self.time_period = time_period
        self.duration = duration
        # Epoch
        self.epoch_date = epoch_date
        self.epoch_time = epoch_time
        # End
        # Date
        if end_date == '':
            self.end_date = None
        else:
            self.end_date = dt.strptime(end_date, Std.input_d_format).date()
        # Time
        if end_time == '':
            self.end_time = None
        else:
            self.end_time = dt.strptime(end_time, Std.input_t_format).time()

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
            # end date
            if json_obj[Std.Keys.end_date] is not '':
                self.end_date = dt.strptime(json_obj[Std.Keys.end_date], Std.std_d_format).date()
                del json_obj[Std.Keys.end_date]
            else:
                self.end_date = None
                del json_obj[Std.Keys.end_date]
            # end time
            if json_obj[Std.Keys.end_time] is not '':
                self.end_time = dt.strptime(json_obj[Std.Keys.end_time], Std.std_t_format).time()
                del json_obj[Std.Keys.end_time]
            else:
                self.end_time = None
                del json_obj[Std.Keys.end_time]

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
                # epoch_time
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

            # end_date
            if self.end_date is not None:
                description[Std.Keys.end_date] = self.end_date.strftime(Std.std_d_format)
            else:
                description[Std.Keys.end_date] = ''

            # end_time
            if self.end_time is not None:
                description[Std.Keys.end_time] = self.end_time.strftime(Std.std_t_format)
            else:
                description[Std.Keys.end_time] = ''

            # misc
            for key in self.misc:
                description[key] = self.misc[key]

            self.description = json.dumps(description)
        except AttributeError:
            return False

        return self.description

    def __str__(self):
        return self.description

    def is_non_repeating(self):
        """
        :return: True if non-repeating , False if repeating
                and -1 if exception occurs
        """
        try:
            # time_period
            if self.time_period.days == 0 and self.time_period.seconds == 0:
                return True
            else:
                return False
        except ValueError:
            return -1
        except KeyError:
            return -1
        except AttributeError:
            return -1

    def is_task(self):
        """
        :return: True if task , False if event
                and -1 if exception occurs
        """
        try:
            # time_period
            if self.duration.days == 0 and self.duration.seconds == 0:
                return True
            else:
                return False
        except ValueError:
            return -1
        except KeyError:
            return -1
        except AttributeError:
            return -1

    def get_end_datetime(self):
        """
        :return:
            Non-Repeating Piece : None
            Repeating Piece : None if end not specified
                            End datetime if specified
        """
        if self.is_non_repeating():
            return None
        else:
            if self.end_date is not None and self.end_time is not None:
                return dt.combine(self.end_date, self.end_time)
            else:
                return None

    def get_stub_which_intersects(self, epoch, lb, ub):
        """
        Assumes proper params are given
        :param epoch datetime
        :param lb datetime
        :param ub datetime
        :return: Stub Dictionary if the given stub of this piece intersects with the [range],
                 None if not
                 -1 if exception occurs
        """
        try:
            stub = None
            # Epoch End of Stub are determined
            end = epoch + self.duration
            # If Stub Intersects With Range
            if lb <= epoch <= ub or lb <= end <= ub or epoch <= lb <= end or epoch <= ub <= end:
                stub_epoch = max([lb, epoch])
                stub_end = min([end, ub])
                stub_tag = self.tag
                stub_comment = self.comment
                stub_pk = self.pk
                stub = {
                    'epoch': stub_epoch,
                    'end': stub_end,
                    'tag': stub_tag,
                    'pk': stub_pk,
                    'comment': stub_comment,
                    'errand_pk': self.errand_id,
                    'color': color_map(self.errand_id, self.pk)
                }
            return stub
        except ValueError:
            return -1
        except KeyError:
            return -1
        except AttributeError:
            return -1
