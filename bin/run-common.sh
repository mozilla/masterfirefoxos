#!/bin/bash

./manage.py collectstatic --noinput -c
./manage.py syncdb --noinput
./manage.py compilemessages
