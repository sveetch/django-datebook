
=========
Changelog
=========

Version 1.2.0 - Unreleased
--------------------------

* Added support for Django 1.8;
* Dropped support for Django 1.7;
* Updated ``setup.py``;
* Fixed crumbs for new Autobreadcrumbs 2.x API;
* Use ``importlib`` Python module instead of deprecated ``django.utils.importlib``;
* Fixed ``DayEntryBaseFormView.get_form`` since ``FormMixin.get_form`` has changed;

Version 1.1.0 - 2016/10/26
--------------------------

* Added support for Django 1.7;
* Dropped support for Django 1.6;
* Moved old south migrations directory ``migrations`` to ``south_migrations``;
* Added initial Django migrations in ``migrations`` directory;
* Fixed usage of future ``cycle`` template tags;
* Updated ``setup.py``;

Version 1.0.0 - 2016/10/24
--------------------------

This is a last working release for Django ``1.6.x``.

* Fixed dependancies to the last right knowed working versions.
* Fixed README for install process;
