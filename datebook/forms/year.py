# -*- coding: utf-8 -*-
"""
Forms for year forms
"""
import datetime

from django import forms
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

from crispy_forms.helper import FormHelper
from crispy_forms_foundation.layout import Submit

from datebook.models import Datebook
from datebook.forms import CrispyFormMixin

class DatebookYearForm(CrispyFormMixin, forms.Form):
    """
    Datebook year form
    """
    crispy_form_helper_path = 'datebook.forms.crispies.year_helper'
    
    def __init__(self, author, queryset, *args, **kwargs):
        self.author = author
        
        super(DatebookYearForm, self).__init__(*args, **kwargs)
        super(forms.Form, self).__init__(*args, **kwargs)
        
        self.today = datetime.date.today()
        existing_years = [item.year for item in queryset]
        available_years = [(k, k) for k in range(self.today.year-3, self.today.year+4) if k not in existing_years]
        
        self.fields['year'] = forms.ChoiceField(label=_('year'), choices=available_years)
    
    def save(self, *args, **kwargs):
        year = int(self.cleaned_data['year'])
        # Default opened datebook is for the first month of the given year
        period = [year, 1, 1]
        # Open the datebook for the current month if the given year is the current year
        if year == self.today.year:
            period = [year, self.today.month, 1]
            
        instance = Datebook(
            author=self.author,
            period=datetime.date(*period)
        )
        instance.save()
        
        return instance
