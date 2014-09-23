# -*- coding: utf-8 -*-
"""
Application Crumbs
"""
from autobreadcrumbs import site
from django.utils.translation import ugettext_lazy

site.update({
    'datebook:index': ugettext_lazy('Datebooks'),
    'datebook:create': ugettext_lazy('Create a datebook'),
    'datebook:author-detail': '{{ author.username }}',
    'datebook:year-detail': '{{ year }}',
    'datebook:month-detail': '{{ target_date|date:"F" }}',
    'datebook:day-add': ugettext_lazy('Add day {{ day }}'),
    'datebook:day-edit': ugettext_lazy('Edit day {{ day }}'),
})
