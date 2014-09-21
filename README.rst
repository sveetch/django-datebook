.. _Django: https://www.djangoproject.com/
.. _South: http://south.readthedocs.org/en/latest/
.. _autobreadcrumbs: https://github.com/sveetch/autobreadcrumbs
.. _django-braces: https://github.com/brack3t/django-braces/
.. _django-guardian: https://github.com/lukaszb/django-guardian
.. _django-crispy-forms: https://github.com/maraujop/django-crispy-forms
.. _crispy-forms-foundation: https://github.com/sveetch/crispy-forms-foundation

Introduction
============

Django datebook is.. a datebook !

This aims to manage user datebooks by months. A datebook contain day entries where you can add details, start and stop working hours, vacation, etc..

This does not aims to reproduce some advanced apps like Google calendar or alike, datebook is simple and will have a particular workflow for our needs at `Emencia <http://emencia.com>`_.


Links
-----

* Download his `PyPi package <https://pypi.python.org/pypi/django-datebook>`_;
* Clone it on his `Github repository <https://github.com/sveetch/django-datebook>`_;

Requires
--------

* `Django`_ >= 1.5;
* `autobreadcrumbs`_ >= 1.0;
* `django-braces`_ >= 1.2.0,<1.4;
* `crispy-forms-foundation`_ >= 0.3.5;

Optionnally :

* `South`_ to perform database migrations for next releases;

Install
=======

Add it to your installed apps in settings : ::

    INSTALLED_APPS = (
        ...
        'datebook',
        ...
    )

Finally mount its urls in your main ``urls.py`` : ::

    urlpatterns = patterns('',
        ...
        (r'^datebook/', include('datebook.urls')),
        ...
    )

Usage
=====

**Datebooks are monthly** so each datebook object represents a unique month for a specific year. And **datebook contains day entries** where you can fill start and stop time, eventually the pause time and some optional text content to describe day activities.

For day entries, **start and stop time represents times for starting and ending work**, they will determine the worked time for the day.

**Pause time represents the time that was not worked between start/stop time** and so will be substracted from the total worked time.

Day entries can be marked as *vacation*, **vacated days will never be used to calculate the total worked time** for the month and their content is hided if any.

Permissions
-----------

At least to access to datebook views, users have to be logged in, there is no anonymous access.

Basic users can see all datebooks and can read their day entries, but they can't add or edit datebooks that they don't own and quite naturally they can't add/edit day entries only on their own datebooks.

For admin management there is some available permissions :

* 'Can add datebook' : used to create datebook for any user;
* 'Can change datebook' : used to edit datebook for any user;
* 'Can add day entry' : used to create day entries for any user's datebook;
* 'Can change day entry' : used to change day entries for any user's datebook;
