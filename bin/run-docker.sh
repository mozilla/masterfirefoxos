#!/bin/sh


if [ -e ./.git/HEAD ]
then
    cp ./.git/HEAD /app/masterfirefoxos/base/static/revision.txt
else
    echo $GIT_SHA > /app/masterfirefoxos/base/static/revision.txt
fi

./bin/run-common.sh
./manage.py collectstatic --noinput
uwsgi --master --wsgi masterfirefoxos.wsgi --http 0.0.0.0:80
