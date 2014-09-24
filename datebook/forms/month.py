# -*- coding: utf-8 -*-
"""
Forms for month forms
"""
from django import forms
from django.utils.translation import ugettext as _

from crispy_forms.helper import FormHelper
from crispy_forms_foundation.layout import Submit

from datebook.models import Datebook
from datebook.forms import CrispyFormMixin

class DatebookForm(CrispyFormMixin, forms.Form):
    """
    Datebook form
    """
    crispy_form_helper_path = 'datebook.forms.crispies.month_helper'
    
    def __init__(self, *args, **kwargs):
        self.available_users = kwargs.pop('available_users', [])
        super(DatebookForm, self).__init__(*args, **kwargs)
        super(forms.Form, self).__init__(*args, **kwargs)
        
        self.fields['owner'] = forms.ModelChoiceField(label=_('owner'), queryset=self.available_users, empty_label=None)
        self.fields['period'] = forms.DateField(label=_('period'))
    
    def clean_period(self):
        period = self.cleaned_data['period']
        period = period.replace(day=1)
        
        return period
    
    def save(self, *args, **kwargs):
        instance = Datebook(
            author=self.cleaned_data['owner'],
            period=self.cleaned_data['period']
        )
        instance.save()
        
        return instance
