# -*- coding: utf-8 -*-
"""
Forms for day forms
"""
from django import forms
from django.utils.translation import ugettext as _

from datebook.models import DayEntry, DayModel
from datebook.forms.day import DATETIME_FORMATS, DayBaseFormMixin
from datebook.forms import CrispyFormMixin

class DayToDayModelForm(DayBaseFormMixin, CrispyFormMixin, forms.ModelForm):
    """
    DayModel form
    """
    crispy_form_helper_kwargs = {'day_to_model_mode': True}
    #crispy_form_helper_path = 'datebook.forms.crispies.day_helper'

    def __init__(self, author, *args, **kwargs):
        self.author = author
        self.dayentry = kwargs.pop('dayentry', None)
        self.daydate = kwargs.pop('day_date', None)
        
        # Args to give to the form layout method
        self.crispy_form_helper_kwargs.update({
            'form_action': kwargs.pop('form_action'),
        })
        
        # Fill initial datas
        kwargs = self.fill_initial_data(*args, **kwargs)
        
        super(DayToDayModelForm, self).__init__(*args, **kwargs)
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        
        # Init some special fields
        kwargs = self.init_fields(*args, **kwargs)
    
    def save(self, *args, **kwargs):
        instance = super(DayToDayModelForm, self).save(commit=False, *args, **kwargs)
        instance.start = self.cleaned_data['start_datetime']
        instance.stop = self.cleaned_data['stop_datetime']
        instance.author = self.author
        instance.save()
        
        return instance
    
    class Meta:
        model = DayModel
        exclude = ('author', 'start', 'stop')
        widgets = {
            'pause': forms.TimeInput(format=DATETIME_FORMATS['input_time_formats'][0]),
            'overtime': forms.TimeInput(format=DATETIME_FORMATS['input_time_formats'][0]),
        }