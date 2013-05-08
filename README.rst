Django datebook is.. a datebook !

This aims to manage user datebooks by months. A datebook contain day entries where you can add details, start and stop working hours, vacation, etc..

This does not aims to reproduce some advanced apps like Google calendar or alike, datebook is simple and will have a particular workflow for our needs at `Emencia <http://emencia.com>`_.

Actually this is only a prototype, more details to come..

Foundation requirements
=======================

Made usage of components :

* Buttons;
* Form and Custom form;
* A mobile grid in 5 columns ($mobileTotalColumns: 5);

TODO
====

* User permission, restriction access, etc..;
* Better ergonomy;
* Add "DayEntry templates" model to fill day entries content from a template string;
* Add "Reminder" model which can be global reminder for all datebooks, or just reminder associated for a single datebook (~=month year);
* i18n and FR translations;
