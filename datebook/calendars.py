# -*- coding: utf-8 -*-
"""
Calendar widgets
"""
import datetime
from calendar import TextCalendar, LocaleHTMLCalendar, _localized_day

class DatebookCalendar(TextCalendar):
    """
    Simple inherit from "TextCalendar" to fill calendars with datas from Datebook(s)
    
    Format methods generally return lists to be used within templates, not for 
    plain/text like TextCalendar
    """
    cssclasses = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
    
    def formatweekheader(self):
        """
        Return a list of tuples ``(CLASSNAME, LOCALIZED_NAME)``
        """
        return [(self.cssclasses[i], _localized_day('%A')[i]) for i in self.iterweekdays()]

    def formatmonth(self, theyear, themonth, dayentries=None, current_day=None, withyear=True):
        """
        Return a list of weeks, each week is a list of day infos as dict
        """
        # Make a dict from the day entries, indexed on the date object
        entries_map = dict(map(lambda x: (x.activity_date, x), dayentries or []))
        # Walk in the weeks of the month to fill days with their associated DayEntry 
        # instance if any
        month = []
        for a, week in enumerate(self.monthdatescalendar(theyear, themonth)):
            month.append([])
            for i, day in enumerate(week):
                obj = None
                if day in entries_map: 
                    obj = entries_map.pop(day)
                month[a].append({
                    'date': day,
                    'entry': obj,
                    'noday': not(day.month==themonth),
                    'is_current': day==current_day,
                })
        return month
