Documentation Versions and Languages
====================================

Adding new Versions of the Documentation
----------------------------------------

To add more Versions of MasterFirefoxOS Documentation you need to create
the corresponding CMS pages and edit settings. For example to add
version 2.0 based on version 1.3T::

1. Go to /admin/page/page
2. Select the root page of version 1.3T
3. Select `Copy tree` from `Action` drop-down and click `Go`.

.. image:: images/copy-tree.png

Step three will copy all pages of version 1.3T into a new tree

.. image:: images/copy-tree-done.png

4. Edit the copied root page and set `title` to `Master Firefox OS`
   and `slug` to `2-0`.

   .. note::

      For slug use dashes instead of dots.

5. Add in `masterfirefoxos.settings.base`::

     VERSIONS_LOCALE_MAP['2.0'] = {
       'slug': '2-0',
       'locales': [
     ]}

And you're done. Edit the content and once you're ready activate
locales for translation. Read `Managing the Versions of Documentation
per locale`_.


Adding new locales
------------------

To add more locales append a tuple with locale code and locale name in
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


Managing the Versions of Documentation per locale
------------------------------------------------

A locale gets activated once it gets linked with a Version of the
Documentation. For example to link locale `foo` with version `1.1` edit
`masterfirefoxos.settings.base.VERSIONS_LOCALE_MAP`::

  VERSIONS_LOCALE_MAP['1.1'] = {
    'slug': '1-1',
    'locales': [
        'en', 'foo'
    ]}

.. note::

   If you need to add a new version, read the `Adding new Versions of
   the Documentation`_.

.. note::

   Check if the locale is also in the `pending_locales` list and
   remove it.

If locale `foo` is still work in progress (e.g. translations are not
complete yet) instead of appending the `locales` list, add it to
`pending_locales` list::

  VERSIONS_LOCALE_MAP['1.1'] = {
    'slug': '1-1',
    'locales': [
        'en'
    ],
    'pending_locales': [
        'foo'
    ]}

This will ensure that localization strings get generated but it will
not display on the site.


Extracting strings
------------------

MasterFirefoxOS stores strings for localization in three different places:

  * Python files (.py)
  * HTML files (.html)
  * In the database

Python and HTML files are automatically handled by Django's
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

The generated po files contain strings for all versions of the CMS
content. The final step is to keep only the strings from the versions
of the CMS content activated per locale::

  ./manage.py runscript cleanup_po


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
