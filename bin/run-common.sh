#!/bin/bash

./manage.py syncdb --noinput
./manage.py compilemessages
./manage.py runscript create_db_locales > /dev/null 2>&1 &
