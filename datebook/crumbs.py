# -*- coding: utf-8 -*-
"""
Application Crumbs
"""
from autobreadcrumbs import site
from django.utils.translation import ugettext_lazy

site.update({
    'datebook-index': ugettext_lazy('Datebooks'),
    
    'datebook-author': ugettext_lazy('{{ author.get_full_name }}'),
    'datebook-author-year': ugettext_lazy('{{ year }}'),
    'datebook-author-month': ugettext_lazy('{{ datebook.period|date:"F" }}'),
    #'datebook-author-month-form': ugettext_lazy('Form'),
    'datebook-author-month-week': ugettext_lazy('Week {{ week }}'),
})
