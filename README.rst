.. _Django: https://www.djangoproject.com/
.. _South: http://south.readthedocs.org/en/latest/
.. _autobreadcrumbs: https://github.com/sveetch/autobreadcrumbs
.. _django-braces: https://github.com/brack3t/django-braces/
.. _rstview: https://github.com/sveetch/rstview
.. _Django-CodeMirror: https://github.com/sveetch/djangocodemirror
.. _django-crispy-forms: https://github.com/maraujop/django-crispy-forms
.. _crispy-forms-foundation: https://github.com/sveetch/crispy-forms-foundation
.. _Arrow: https://github.com/crsmithdev/arrow

Introduction
============

Django datebook is.. a datebook !

This aims to manage user datebooks by months. A datebook contain day entries where you can add details, start and stop working hours, vacation, etc..

This does not aims to reproduce some advanced apps like Google calendar or alike, datebook is simple and will have a particular workflow for our needs at `Emencia <http://emencia.com>`_.


Links
*****

* Download his `PyPi package <https://pypi.python.org/pypi/django-datebook>`_;
* Clone it on his `Github repository <https://github.com/sveetch/django-datebook>`_;

Requires
********

* `Django`_ >=1.7, <1.8;
* `autobreadcrumbs`_ >= 1.0, <2.0.0;
* `django-braces`_ >= 1.2.0,<1.4;
* `crispy-forms-foundation`_ >= 0.5.3;
* `Arrow`_;


Optionnally
***********

* If you want to use the shipped *Text markup* integration :

  * `rstview`_ >= 0.2, <0.4.0;
  * `Django-CodeMirror`_ >= 0.9.7, <1.0.0;

`South`_ usage has been dropped in favor of Django migrations;

Install
=======

Install it from PyPi: ::

    pip install django-datebook

Add it to your installed apps in settings : ::

    INSTALLED_APPS = (
        ...
        'django_assets',
        'crispy_forms',
        'crispy_forms_foundation',
        'autobreadcrumbs',
        'datebook',
        ...
    )

Append context processor in settings : ::

    TEMPLATE_CONTEXT_PROCESSORS = (
        ...
        'autobreadcrumbs.context_processors.AutoBreadcrumbsContext',
        ...
    )

Add required settings (into your project settings):

.. sourcecode:: python

    # Add 'foundation-5' layout pack
    CRISPY_ALLOWED_TEMPLATE_PACKS = ('bootstrap', 'uni_form', 'bootstrap3', 'foundation-5')
    # Default layout to use with "crispy_forms"
    CRISPY_TEMPLATE_PACK = 'foundation-5'

    from datebook.settings import *

(Also you can override some of its settings, see ``datebook.settings`` for more details).

Then in your ``urls.py`` : ::

    from django.conf.urls import patterns, include, url
    import autobreadcrumbs
    autobreadcrumbs.autodiscover()

    urlpatterns = patterns('',
        url(r'^datebook/', include('datebook.urls', namespace='datebook')),
    )

Finally you will need to read Django-datebook templates to know about required
template blocks and inheritance in your project templates.

Text markup
***********

Default behavior configured in settings is to not use any Markup syntax usage.

But if you want you can configure some settings to use a Markup syntax renderer and a form field to use a specific editor.

This can be done with the following settings:

.. sourcecode:: python

    # Text markup renderer
    DATEBOOK_TEXT_MARKUP_RENDER = None # Default, no renderer

    # Field helper for texts in forms
    DATEBOOK_TEXT_FIELD_HELPER_PATH = None # Default, just a CharField

    # Template to init some Javascript for texts in forms
    DATEBOOK_TEXT_FIELD_JS_TEMPLATE = None # Default, no JS template

    # Validator helper for texts in forms
    DATEBOOK_TEXT_VALIDATOR_HELPER_PATH = None # Default, no markup validation

They are the default values in the datebook settings.

Explanations
------------

**DATEBOOK_TEXT_FIELD_HELPER_PATH**
    a function that will be used to define a form field to use for text.

    Signature is ``get_text_field(form_instance, **kwargs)`` where:

    * ``form_instance`` is the Form instance where it will be used from;
    * ``kwargs`` is a dict containing all default named arguments to give to the field. These default arguments are ``label`` for the field label name and ``required``  that is ``True`` (you should never change this);

    This should return an instanciated form field that must act as a ``CharField``.

**DATEBOOK_TEXT_VALIDATOR_HELPER_PATH**

    A function that will be used to clean value on the form field text;

    Signature is ``clean_restructuredtext(form_instance, content)`` where:

    * ``form_instance`` is the Form instance where it will be used from;
    * ``content`` is the value to validate;

    Act like a Django form field cleaner method, this should return the cleaned value and eventually raise a validation error if needed.

**DATEBOOK_TEXT_MARKUP_RENDER_TEMPLATE**

    A template to include to render text value with some markup syntax. It will have access to the page context with an additional value named ``content`` that will be the text to render;

**DATEBOOK_TEXT_FIELD_JS_TEMPLATE**

    A template to include with forms when your custom form field require some Javascript to initialize it. It will have access to page context with an additional value named ``field`` that will be the targeted form field;

All these settings are only used with forms and template managing ``Datebook.notes`` and ``DayBase.content`` models attributes.

Example
-------

There are the settings to use the shipped Markup syntax renderer and editor, disabled by default but that you can easily enable in your settings:

.. sourcecode:: python

    # Field helper for texts in forms
    DATEBOOK_TEXT_FIELD_HELPER_PATH = "datebook.markup.get_text_field" # Use DjangoCodeMirror

    # Validator helper for texts in forms
    DATEBOOK_TEXT_VALIDATOR_HELPER_PATH = "datebook.markup.clean_restructuredtext" # Validation for RST syntax (with Rstview)

    # Template to init some Javascript for texts in forms
    DATEBOOK_TEXT_FIELD_JS_TEMPLATE = "datebook/markup/_text_field_djangocodemirror_js.html" # Use DjangoCodeMirror

    # Text markup renderer
    DATEBOOK_TEXT_MARKUP_RENDER_TEMPLATE = "datebook/markup/_text_markup_render.html" # Use Rstview renderer

Read their source code to see how they work in detail.

.. warning:: Before enabling these settings you must install `rstview`_ and `Django-CodeMirror`_, see optional requirements to have the right versions to install.

Usage
=====

**Datebooks are monthly** so each datebook object represents a unique month for a specific year. And **datebook contains day entries** where you can fill start and stop time, eventually the pause time and some optional text content to describe day activities.

For day entries, **start and stop time represents times for starting and ending work**, they will determine the worked time for the day.

**Pause time represents the time that was not worked between start/stop time** and so will be substracted from the total worked time.

**Overtime represents the extra time that is over the working hours**, it does not affect the worked time.

Day entries can be marked as *vacation*, **vacated days will never be used to calculate the total worked time** for the month and their content is hided if any.

Also, future days (days that are bigger or equal to the current day) are not used to calculate month totals (worked hours, overtime and vacations).

Permissions
***********

At least to access to datebook views, users have to be logged in, there is no anonymous access.

Basic users can see all datebooks and can read their day entries, but they can't add or edit datebooks that they don't own and quite naturally they can't add/edit day entries only on their own datebooks.

For admin management there is some available permissions :

* 'Can add datebook' : used to create datebook for any user;
* 'Can change datebook' : used to edit datebook for any user;
* 'Can add day entry' : used to create day entries for any user's datebook;
* 'Can change day entry' : used to change day entries for any user's datebook;

Permission level object (like with django-guardian) is not planned because the goal is not to share datebook between users. Only datebook owner should edit its entry and all datebook are visible for any logged users, because a team should be aware of everyone datebooks.

Day models
**********

Often you would need to repeatedly fill your days with the approximately same content and so to avoid this there is *Day models*.

You can create a *Day model* from an existing day in your calendars, its content will be saved as a model and then you can use it to fill any another days in your calendar.

You can have multiple models, but they are allways for an unique user, models are not shareable through other users.

To fill days with a model, just go into a month calendar, open the models menu, select the day to fill, select the model to use and submit, existing days will be overwrited with model contents and empty selected days will be created with the model contents.

When filling days, default behavior does not use the model content text to fill the days, use the checkbox within the assignment form to use it.

Credits
=======

Collaborators
    * `slothyrulez <https://github.com/slothyrulez>`_ for Spanish translation;
For the "Sun umbrella" icon in webfont
    Icon made by `Freepik <http://www.freepik.com>`_ from `www.flaticon.com <http://www.flaticon.com>`_ is licensed under `CC BY 3.0 <http://creativecommons.org/licenses/by/3.0/>`_.
Other icons in webfont
    Comes from various sets on `IcoMoon <https://icomoon.io>`_.