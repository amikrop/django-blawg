django-blawg
============

Simple blogging application
---------------------------

**django-blawg** is a very basic blogging app that was mainly made to
practice generic views and mixins. It supports multiple blogs
for users, date-based listings and comments. An already existing
user authentication system is assumed and utilized. **django-blawg** is
not optimized or built for large-scale usage.

Installation
------------

- Download and install from PyPI:

.. code::

    pip install django-blawg

This will also install `django-mptt` and `django-autoslug`, as they are dependencies.

- Add it to your `INSTALLED_APPS`, as well as `'mptt'`:

.. code:: python

    INSTALLED_APPS = (
        ...
        'mptt',
        ...
        'blawg',
        ...
    )

- Include the urlconf of the app in your project's urls.py:

.. code:: python

    from django.conf.urls import url, include

    urlpatterns = [
        ...
        url(r'blog/', include('blawg.urls', namespace='blawg')),
        ...
    ]

Of course, you can put it under any url you want,
like `r''` or `r'^mysite/myblog/'`.

Usage
-----

The starting URL is some user's username, his home page, which lists
the user's blogs. The root URL redirects to the currently logged in
user's home page.

Settings
--------

All of the app settings are optional but you may want to modify them
to customize to your needs.

- `BLAWG_TITLE_MAX_LENGTH`: Maximum allowed characters for blog and entry title.

    Default: `100`

- `BLAWG_DESCRIPTION_MAX_LENGTH`: Maximum allowed characters for blog description.

    Default: `200`

- `BLAWG_GUEST_NAME_MAX_LENGTH`: Maximum allowed characters for anonymous commenter name.

    Default: `30`

- `BLAWG_FORBIDDEN_SLUGS`: List of words not allowed to be used as slugs.

    Default: `['create', 'update', 'delete']`

- `BLAWG_SLUG_MODIFIER`: String to be appended to an invalid slug.

    Default: `'-'`

License
-------

BSD

Author
------

Aristotelis Mikropoulos *<amikrop@gmail.com>*
