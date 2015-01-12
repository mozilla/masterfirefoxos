#!/bin/bash

./manage.py syncdb --noinput
./manage.py compilemessages
