# -*- coding: utf-8 -*-
import calendar

def split_seconds_to_clock(seconds):
    """Convert a time in seconds to a string like '15:22:01'"""
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return {
        'hour': h,
        'minute': m,
        'second': s
    }

def format_seconds_to_clock(seconds):
    """Convert a time in seconds to a string like '15:22:01'"""
    #return "%d:%02d:%02d" % split_second_to_clock(seconds)
    return "{hour}:{minute:02}".format(**split_seconds_to_clock(seconds))

def time_to_seconds(timeobj):
    """Convert a time to seconds"""
    return (timeobj.hour*60*60)+(timeobj.minute*60)+timeobj.second

def timedelta_to_seconds(delta):
    """Convert a timedelta to seconds, only taking care of days and seconds (that is left unchanged)"""
    return (delta.days*24*60*60)+delta.seconds

def week_from_date(dt, start=1):
    """
    Return the week number of the month from a datetime.Date, this is index on 1 by 
    default, use 'start' argument to change this
    """
    for week_no, week in enumerate(calendar.Calendar().monthdayscalendar(dt.year, dt.month), start=start):
        if dt.day in week:
            return week_no
    # This should never happend
    raise ValueError

def get_day_weekno(weeks, dayno):
    """
    Given a week list of day tuples, find and return the week number (index 
    on zero) for that the day number belong to
    """
    for i, daysno in enumerate(weeks, start=0):
        if dayno in daysno:
            return i
    # This should never happend
    raise ValueError
