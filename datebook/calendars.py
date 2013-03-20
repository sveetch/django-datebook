# -*- coding: utf-8 -*-
"""
Calendar widgets
"""
from calendar import LocaleHTMLCalendar

class DatebookHTMLCalendar(LocaleHTMLCalendar):
    """
    HTML render for a Calendar
    
    Should be better to reimplement it in a clean templatetag using a template,
    or as a "DatebookArrayCalendar" that could be passed in template where we can walk 
    in the elements to display a calendar with more flexibility.
    """
    html_table_attrs = ['class="datebook-calendar-month"']
    
    def __init__(self, day_items=None, current_day=None, firstweekday=0, locale=None):
        self.day_items = day_items
        self.current_day = current_day
        super(DatebookHTMLCalendar, self).__init__(firstweekday=firstweekday, locale=locale)
    
    def formatmonthname(self, theyear, themonth, withyear=True):
        return ''

    def formatmonth(self, theyear, themonth, withyear=True):
        """
        Return a formatted month as a table.
        """
        v = []
        a = v.append
        a('<table {0}>'.format(" ".join(self.html_table_attrs)))
        a('\n')
        a(self.formatweekheader())
        a('\n')
        for week in self.monthdays2calendar(theyear, themonth):
            a(self.formatweek(week))
            a('\n')
        a('</table>')
        a('\n')
        return ''.join(v)

    def formatday(self, day, weekday):
        """
        Subclassing original method to inject data in day cell
        """
        # If empty cell or no datas given, use the original behavior
        if day == 0 or self.day_items is None:
            return super(DatebookHTMLCalendar, self).formatday(day, weekday)
        
        attrs = ""
        
        _cssclasses = self.cssclasses[weekday]
        if self.current_day and self.current_day == day:
            _cssclasses += " current"
        
        # Fill in the day cell with its datas
        _html_content = ""
        if day in self.day_items:
            _cssclasses += " entry"
            _html_content = u"""<p class="working-hour">{workinghour}</p>
            <div class="content">{content}</div>
            <p class="length">{length}</p>""".format(
                workinghour=self.day_items[day].get_working_hours(),
                length=self.day_items[day].get_elapsed_time(),
                # TODO: Parse with ReStructuredText
                content=self.day_items[day].content,
            )
        
        return u'<td class="{classes}"{attrs}><div class="container"><span class="daylabel">{day}</span>{html_content}</div></td>'.format(
            classes=_cssclasses,
            attrs=attrs,
            day=day,
            html_content=_html_content,
        )
