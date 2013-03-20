# -*- coding: utf-8 -*-
def format_second_to_clock(seconds):
    """Convert a time in seconds to a string like '15:22:01'"""
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "%d:%02d:%02d" % (h, m, s)

def time_to_seconds(timeobj):
    """Convert a time to seconds"""
    return (timeobj.hour*60*60)+(timeobj.minute*60)+timeobj.second

def timedelta_to_seconds(delta):
    """Convert a timedelta to seconds, only taking care of days and seconds (that is left unchanged)"""
    return (delta.days*24*60*60)+delta.seconds
