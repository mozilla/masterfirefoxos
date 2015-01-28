import os

from django.conf import settings

from masterfirefoxos.base.utils import pages_l10n_template


def run(*args):
    if args:
        filename = args[0]
    else:
        filename = os.path.join(settings.BASE_DIR, 'db-strings.txt')
    print(filename)
    template_text = pages_l10n_template()
    if filename == '-':
        print(template_text)
    else:
        with open(filename, 'w') as f:
            f.write(template_text)
