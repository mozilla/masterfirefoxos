import os

from django.conf import settings
from django.core.management.base import BaseCommand

from masterfirefoxos.base.utils import pages_l10n_template


class Command(BaseCommand):
    args = '<filename>'
    help = 'Extract strings from db to text file for l10n'

    def handle(self, *args, **options):
        if args:
            filename = args[0]
        else:
            filename = os.path.join(settings.BASE_DIR, 'db-strings.txt')
        template_text = pages_l10n_template()
        if filename == '-':
            self.stdout.write(template_text)
        else:
            with open(filename, 'w') as f:
                f.write(template_text)
        
