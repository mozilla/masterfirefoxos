#!/bin/bash
set -ex

# Create a temporary virtualenv to install fig
TDIR=`mktemp -d`
virtualenv $TDIR
. $TDIR/bin/activate
pip install fig

# Run Tests
fig --project-name jenkins${JOB_NAME}${BUILD_NUMBER} run -T web ./manage.py test -v 2

# Delete virtualenv
rm -rf $TDIR
