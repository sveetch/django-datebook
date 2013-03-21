# -*- coding: utf-8 -*-
"""
Application Crumbs
"""
from autobreadcrumbs import site
from django.utils.translation import ugettext_lazy

site.update({
    'datebook-index': ugettext_lazy('Agendas'),
    'datebook-year': ugettext_lazy('Year {{ year }} - {{ author.get_full_name }}'),
    'datebook-month': ugettext_lazy('{{ datebook.period|date:"F Y" }} - {{ datebook.author.get_full_name }}'),
    'datebook-month-week': ugettext_lazy('{{ datebook.period|date:"F Y" }} week {{ month_week }} - {{ datebook.author.get_full_name }}'),
})
