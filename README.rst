.. _Django: https://www.djangoproject.com/
.. _South: http://south.readthedocs.org/en/latest/
.. _autobreadcrumbs: https://github.com/sveetch/autobreadcrumbs
.. _django-braces: https://github.com/brack3t/django-braces/
.. _django-guardian: https://github.com/lukaszb/django-guardian
.. _django-crispy-forms: https://github.com/maraujop/django-crispy-forms

Introduction
============

Django datebook is.. a datebook !

This aims to manage user datebooks by months. A datebook contain day entries where you can add details, start and stop working hours, vacation, etc..

This does not aims to reproduce some advanced apps like Google calendar or alike, datebook is simple and will have a particular workflow for our needs at `Emencia <http://emencia.com>`_.

Actually this is only a prototype, more details to come..


Links
-----

* Download his `PyPi package <https://pypi.python.org/pypi/django-datebook>`_;
* Clone it on his `Github repository <https://github.com/sveetch/django-datebook>`_;

Requires
--------

* `Django`_ >= 1.5;
* `autobreadcrumbs`_ >= 1.0;
* `django-braces`_ >= 1.2.0,<1.4;
* `django-crispy-forms`_ >= 1.4.0;
* `django-guardian`_ >= 1.2.0;

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
