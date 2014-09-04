"""
Crispy forms layouts
"""
from django import forms
from django.utils.translation import ugettext as _

from crispy_forms.helper import FormHelper
from crispy_forms_foundation.layout import Layout, Fieldset, SplitDateTimeField, Row, Column, Field, InlineField, ButtonHolder, ButtonHolderPanel, Submit

def day_helper(form_tag=True):
    """
    DayEntry's form layout helper
    """
    helper = FormHelper()
    helper.form_action = '.'
    helper.attrs = {'data_abide': ''}
    helper.form_tag = form_tag
    
    helper.layout = Layout(
        Row(
            Column('vacation', css_class='small-12'),
        ),
        Row(
            Column('start_datetime', css_class='small-4 medium-5'),
            Column('pause', css_class='small-4 medium-2'),
            Column('stop_datetime', css_class='small-4 medium-5'),
        ),
        Row(
            Column('content', css_class='small-12'),
        ),
        ButtonHolderPanel(
            Submit('submit', _('Submit')),
            css_class='text-right',
        ),
    )
    
    return helper


def month_helper(form_tag=True):
    """
    Datebook's form layout helper
    """
    helper = FormHelper()
    helper.form_action = '.'
    helper.attrs = {'data_abide': ''}
    helper.form_tag = form_tag
    
    helper.layout = Layout(
        Row(
            Column(
                Field('owner'),
                css_class='small-12 medium-7 hide-label'
            ),
            Column(
                Field('period'),
                css_class='small-12 medium-3 hide-label'
            ),
            Column(
                ButtonHolder(
                    Submit(
                        'submit',
                        _('Submit'),
                        css_class='tiny expand',
                    ),
                    css_class='text-right',
                ),
                css_class='small-12 medium-2'
            ),
            css_class='collapse',
        ),
    )
    
    return helper

def year_helper(form_tag=True):
    """
    Datebook's year form layout helper
    """
    helper = FormHelper()
    helper.form_action = '.'
    helper.form_class = "hide-label right clearfix"
    helper.attrs = {'data_abide': ''}
    helper.form_tag = form_tag
    
    helper.layout = Layout(
        Field(
            'year',
            wrapper_class='left',
        ),
        Submit(
            'submit',
            _('New year'),
            css_class='tiny',
        ),
    )
    
    return helper
