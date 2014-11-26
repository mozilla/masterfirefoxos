Internationalization
====================

Adding new languages
--------------------

To add more languages to masterfirefoxos you need to append a tuple
with locale code and locale name in
`masterfirefox.settings.base.LANGUAGES`. For example to add German
change `LANGUAGES` to::

  LANGUAGES = (
    ('en', ugettext_lazy('English')),
    ('el', ugettext_lazy('Greek')),
    ('de', ugettext_lazy('German')),
  )

Then you need to generate messages for the first time for the added locale::

  ./manage.py makemessages --locale de

.. note::

   It's important to explicitly define the new locale using the
   `--locale` flag when executing the `makemessages` command. Using
   the `-a` flag to make messages for all locales will ignore the new
   locales.


Extracting strings
------------------

MasterFirefoxOS stores strings for localization in three different places:

  * Python files (.py)
  * HTML files (.html)
  * In the database 

Python and HTML files are automatically handled by django's
`makemessages` command. The database strings must first get extracted
into a text file be parsable by `makemessages` command. To extract the
database strings run::

  ./manage.py cron extract_database_strings

.. note::

  Extracted database strings are stored in `db-strings.txt` file. This
  file should *not* be edited manually.

Now all strings are in Python, HTML and Text files that `makemessages`
command can parse. To generate `.po` files for all supported languages
run::

  ./manage.py makemessages -a 

.. warning::

   Always extract database strings before running
   `makemessages`. Failing to do so may remove all database strings
   from `.po` files.


Now you can distributed your `.po` files to the translators.
   

Compile strings
---------------

Given that you have translated `.po` files you need to compile them
into `.mo` files. To do this run the `compilemessages` command::

  ./manage.py compilemessages


This is required step for translations to work.
  

How does database localization work?
------------------------------------

A script iterates through all FeinCMS Pages and through all Content
Types defined in each Page. If a field in the Content Type inherits
the `LocalizableField` class then its contents are saved in a text
file defined in `masterfirefox.base.cron.EXPORT_TO` (currently
`db-strings.txt`).

This text file can be parsed with the standard `makemessages` command
to generate a `.po` file.

The script adds comments with extra information for localizers about
the Page(s) that contain the strings.


Add new localizable database fields
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You need to implement your own `FeinCMS Content Types`_ and instead of
using the standard Django's `TextField` and `CharField` use
`masterfirefoxos.base.fields.LocalizableTextField` and
`masterfirefoxos.base.fields.LocalizableCharField` respectively. For
example to create a FAQ Content Type with a question and answer
localizable fields create the following model::

  import masterfirefoxos.base.fields


  class FAQEntry(models.Model):

    question = fields.LocalizableCharField(max_length=255)
    answer = fields.LocalizableTextField(max_length=255)

    class Meta:
        abstract = True


Both fields will be recognized by `extract_database_strings` script
and will get extracted to `db-strings.txt`.

You will also need a custom `render` method that calls `ugettext` on
each localizable field::

  from django.utils.translation import ugettext as _

  import masterfirefoxos.base.fields

  
  class FAQEntry(models.Model):

    question = fields.LocalizableCharField(max_length=255)
    answer = fields.LocalizableTextField(max_length=255)

    class Meta:
        abstract = True

    def render(self, **kwargs):
        return render_to_string(
            'faqentry.html',
            {
                'question': _(self.question),
                'answer': _(self.answer),
            }
        )



.. _FeinCMS Content Types: https://feincms-django-cms.readthedocs.org/en/latest/contenttypes.html#implementing-your-own-content-types
