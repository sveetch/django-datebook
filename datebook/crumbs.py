# -*- coding: utf-8 -*-
"""
Application Crumbs
"""
from autobreadcrumbs import site
from django.utils.translation import ugettext_lazy

site.update({
    'datebook-index': ugettext_lazy('Datebooks'),
    'datebook-create': ugettext_lazy('Create a datebook'),
    'datebook-author': '{{ author.username }}',
    'datebook-author-year': '{{ year }}',
    'datebook-author-month': '{{ target_date|date:"F" }}',
    'datebook-author-day-add': ugettext_lazy('Add day {{ day }}'),
    'datebook-author-day-edit': ugettext_lazy('Edit day {{ day }}'),
})
