Introduction
============

Django datebook is.. a datebook !

This aims to manage user datebooks by months. A datebook contain day entries where you can add details, start and stop working hours, vacation, etc..

This does not aims to reproduce some advanced apps like Google calendar or alike, datebook is simple and will have a particular workflow for our needs at `Emencia <http://emencia.com>`_.

Actually this is only a prototype, more details to come..

TODO
----

* User permission, restriction access, etc..;
* Better ergonomy;
* Add "DayEntry templates" model to fill day entries content from a template string;
* Add "Reminder" model which can be global reminder for all datebooks, or just reminder associated for a single datebook (~=month year);
* i18n and FR translations;


Links
-----

* Clone it on his `Github repository <https://github.com/sveetch/datebook>`_;

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
