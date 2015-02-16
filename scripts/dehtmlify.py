from legacy import fix_all_locales, split_db_h2s, split_db_h3s
from masterfirefoxos.base.utils import unmangle_pages


def run(*args):
    unmangle_pages()
    split_db_h2s()
    split_db_h3s()
    fix_all_locales()
