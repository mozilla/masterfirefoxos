from legacy import (
    fix_all_locales, fix_double_strong, split_db_h2s, split_db_h3s,
    strip_subheader_ems, strip_all_fields)
from masterfirefoxos.base.utils import unmangle_pages


def run(*args):
    unmangle_pages()
    split_db_h2s()
    split_db_h3s()
    strip_subheader_ems()
    fix_double_strong()
    strip_all_fields()
    fix_all_locales()
