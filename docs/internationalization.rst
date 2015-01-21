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

  ./manage.py runscript db_strings

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

The following command will iterate through all FeinCMS Pages and
through all Content Types defined in each Page, and extract strings
from fields named in each Content Type model's `_l10n_fields`
attribute, and output to a template text file:

  ./manage.py db_strings
  
By default, the command outputs to `db-strings.txt` but accepts an
optional `filename` argument.

This text file can be parsed with `./manage.py makemessages` command
to generate a `.po` file.

We use a custom `render` method that calls `ugettext` on
each localizable field::

  from django.utils.translation import ugettext as _

  class FAQEntry(models.Model):

    question = fields.CharField(max_length=255)
    answer = fields.TextField(max_length=255)
    _l10n_fields = ['question', 'answer']

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
