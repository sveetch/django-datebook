# -*- coding: utf-8 -*-
"""
Model admin
"""
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from models import *

class DatebookAdmin(admin.ModelAdmin):
    ordering = ('-modified',)
    list_filter = ('created', 'modified', 'author')
    list_display = ('period_title', 'author', 'days_count', 'created', 'modified')
    raw_id_fields = ("author",)

    def period_title(self, datebook):
        return datebook
    period_title.short_description = _("month of activity")
    period_title.admin_order_field = 'period'

    def days_count(self, datebook):
        return datebook.dayentry_set.all().count()
    days_count.short_description = _('Days')

class DayBaseAdmin(admin.ModelAdmin):
    def start_time(self, day):
        return day.start.time()
    start_time.short_description = _("start")
    start_time.admin_order_field = 'start'

    def stop_time(self, day):
        return day.stop.time()
    stop_time.short_description = _("stop")
    stop_time.admin_order_field = 'stop'


class DayEntryAdmin(DayBaseAdmin):
    ordering = ('-activity_date',)
    list_filter = ('vacation', 'datebook__author', 'activity_date')
    list_display = ('activity_date', 'datebook_title', 'start_time', 'stop_time', 'pause', 'overtime', 'vacation')
    list_display_links = ('activity_date',)
    raw_id_fields = ("datebook",)
    fieldsets = (
        (_('Date'), {
            'fields': ('datebook', 'activity_date')
        }),
        (_('Time'), {
            'fields': ('vacation', 'start', 'stop', 'pause', 'overtime')
        }),
        (_('Content'), {
            'fields': ('content',),
        }),
    )

    def datebook_title(self, day):
        return "{author} - {period}".format(author=day.datebook.author, period=day.datebook)
    datebook_title.short_description = _("Datebook")
    datebook_title.admin_order_field = 'datebook__author__username'


class DayModelAdmin(DayBaseAdmin):
    ordering = ('author__username', 'title',)
    list_filter = ('author',)
    list_display = ('title', 'author', 'start_time', 'stop_time', 'pause', 'overtime')
    raw_id_fields = ("author",)
    fieldsets = (
        (_('Parameters'), {
            'fields': ('author', 'title')
        }),
        (_('Time'), {
            'fields': ('start', 'stop', 'pause', 'overtime')
        }),
        (_('Content'), {
            'fields': ('content',),
        }),
    )


admin.site.register(Datebook, DatebookAdmin)
admin.site.register(DayEntry, DayEntryAdmin)
admin.site.register(DayModel, DayModelAdmin)
