# -*- coding: utf-8 -*-
"""
Root url's map for application
"""
from django.conf.urls import *

from datebook.views import IndexView
from datebook.views.author import DatebookAuthorView
from datebook.views.year import DatebookYearView
from datebook.views.month import DatebookMonthView, DatebookMonthGetOrCreateView, DatebookMonthCurrentView, DatebookMonthFormView, DatebookNotesFormView
from datebook.views.day import DayEntryFormCreateView, DayEntryDetailView, DayEntryFormEditView, DayEntryCurrentView, DayEntryDeleteFormView
from datebook.views.daymodel import DayModelListView, DayEntryToDayModelFormView, DayModelFormEditView

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='index'),
    
    url(r'^create/$', DatebookMonthFormView.as_view(), name='create'),
    
    url(r'^(?P<author>\w+)/$', DatebookAuthorView.as_view(), name='author-detail'),
    
    url(r'^(?P<author>\w+)/day-models/$', DayModelListView.as_view(), name='day-models'),
    url(r'^(?P<author>\w+)/day-models/(?P<pk>\d+)/$', DayModelFormEditView.as_view(), name='day-model-edit'),
    
    url(r'^(?P<author>\w+)/current-day/$', DayEntryCurrentView.as_view(), name='current-day'),
    url(r'^(?P<author>\w+)/current-month/$', DatebookMonthCurrentView.as_view(), name='current-month'),
    
    url(r'^(?P<author>\w+)/(?P<year>\d{4})/$', DatebookYearView.as_view(), name='year-detail'),
    url(r'^(?P<author>\w+)/(?P<year>\d{4})/add/(?P<month>\d{1,2})/$', DatebookMonthGetOrCreateView.as_view(), name='month-add'),
    
    url(r'^(?P<author>\w+)/(?P<year>\d{4})/(?P<month>\d{1,2})/$', DatebookMonthView.as_view(), name='month-detail'),
    url(r'^(?P<author>\w+)/(?P<year>\d{4})/(?P<month>\d{1,2})/notes/$', DatebookNotesFormView.as_view(), name='month-notes'),
    
    url(r'^(?P<author>\w+)/(?P<year>\d{4})/(?P<month>\d{1,2})/add/(?P<day>\d{1,2})/$', DayEntryFormCreateView.as_view(), name='day-add'),
    
    url(r'^(?P<author>\w+)/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$', DayEntryDetailView.as_view(), name='day-detail'),
    url(r'^(?P<author>\w+)/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/edit/$', DayEntryFormEditView.as_view(), name='day-edit'),
    url(r'^(?P<author>\w+)/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/remove/$', DayEntryDeleteFormView.as_view(), name='day-remove'),
    url(r'^(?P<author>\w+)/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/to-daymodel/$', DayEntryToDayModelFormView.as_view(), name='dayentry-to-daymodel'),
)
