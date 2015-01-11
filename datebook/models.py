# -*- coding: utf-8 -*-
"""
Modèles de données
"""
import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now as tz_now, localtime

from datebook import utils

class Datebook(models.Model):
    """
    Datebook is only for one user (its author) and it is not shared.
    
    A Datebook is for a specific month of a year.
    
    A Datebook is alike "lazy" in the way that its 'DayEntry' are only created 
    when the user fill them and so Datebook are not initialized with all its 
    month's days when created.
    """
    author = models.ForeignKey(User, verbose_name=_('author'))
    created = models.DateTimeField(_('created'), blank=True, editable=False)
    modified = models.DateTimeField(_('last edit'), auto_now=True)
    period = models.DateField(_("month of activity"), blank=False)
    notes = models.TextField(_("content"), max_length=500, blank=True)

    def __unicode__(self):
        return self.period.strftime("%B %Y")

    @models.permalink
    def get_absolute_url(self):
        return ('datebook:month-detail', (), {
            'author': self.author.username,
            'year': self.period.year,
            'month': self.period.strftime('%m'),
        })

    def clean(self):
        """Allways forcing to the first day of the month"""
        self.period = self.period.replace(day=1) 

    def save(self, *args, **kwargs):
        # First create
        if not self.created:
            self.created = tz_now()
        
        super(Datebook, self).save(*args, **kwargs)

    class Meta:
        unique_together = ("author", "period")
        verbose_name = _("Datebook")
        verbose_name_plural = _("Datebooks")


class DayBase(models.Model):
    """
    Base day model
    """
    content = models.TextField(_("content"), max_length=500, blank=True)

    start = models.DateTimeField(_('start'), blank=False) # should default to something like 9h with the dayentry date
    stop = models.DateTimeField(_('stop'), blank=False) # should default to something like 19h with the dayentry date
    pause = models.TimeField(_('pause'), blank=False, default=datetime.time(0, 0))
    overtime = models.TimeField(_('overtime'), blank=False, default=datetime.time(0, 0))

    def get_display_hour(self, timeobj):
        """Formating time "XXhYY" display, minutes are not displayed if they are not > 0"""
        _m = ""
        timeobj = localtime(timeobj)
        if timeobj.minute > 0:
            _m = str(timeobj.minute).rjust(2, "0")
        return _('%(hour)sh%(minute)s') % {'hour': str(timeobj.hour).rjust(2, "0"), 'minute': _m}

    def get_working_hours(self):
        """Display working hours like: '08h to 18h59'"""
        return _('%(start)s to %(stop)s') % {'start': self.get_display_hour(self.start), 'stop': self.get_display_hour(self.stop)}

    def get_elapsed_seconds(self):
        """Return elapsed seconds between start and stop, where pause time has been substracted from"""
        return utils.timedelta_to_seconds((self.stop-self.start))-utils.time_to_seconds(self.pause)

    def get_elapsed_time(self):
        """Return formatted clock for elapsed seconds from 'get_elapsed_seconds'"""
        return utils.format_seconds_to_clock(self.get_elapsed_seconds())

    def get_overtime_seconds(self):
        """Return overtime seconds"""
        return utils.time_to_seconds(self.overtime)

    def get_overtime_time(self):
        """Return formatted clock for overtime seconds from 'get_overtime_seconds'"""
        return utils.format_seconds_to_clock(self.get_overtime_seconds())

    #def clean(self):
        ##DEPRECATED: Stuff below are for the form controller
        #from django.core.exceptions import ValidationError
        ## Stop can't be less than start
        #if self.stop < self.start:
            #raise ValidationError(_("Hour stop can't be less than hour start."))
        ## TODO: Pause time can't be superior to the time of (stop-start)
    
    class Meta:
        abstract = True    


class DayEntry(DayBase):
    """
    Activity day in a Datebook
    """
    datebook = models.ForeignKey(Datebook, verbose_name=_('datebook'))
    activity_date = models.DateField(_('activity day date'), blank=False) # inherit month and year from its Datebook
    vacation = models.BooleanField(_('vacation'), default=False, blank=True, null=False)

    def __unicode__(self):
        if not self.activity_date:
            return _("Empty")
        return self.activity_date.strftime("%d/%m/%Y")

    def clean(self):
        # Inherit the year and month from its datebook
        if hasattr(self, 'datebook'):
            self.activity_date = self.activity_date.replace(month=self.datebook.period.month, year=self.datebook.period.year)

    def save(self, *args, **kwargs):
        # Allways update the datebook
        self.datebook.modified = tz_now()
        self.datebook.save()
        
        super(DayEntry, self).save(*args, **kwargs)

    class Meta:
        unique_together = ("datebook", "activity_date")
        verbose_name = _("day entry")
        verbose_name_plural = _("day entries")


class DayModel(DayBase):
    """
    Day model from an user
    """
    author = models.ForeignKey(User, verbose_name=_('author'))
    title = models.CharField(_("title"), blank=False, max_length=255)

    def __unicode__(self):
        return self.title

    class Meta:
        unique_together = ("author", "title")
        verbose_name = _("day model")
        verbose_name_plural = _("day models")
