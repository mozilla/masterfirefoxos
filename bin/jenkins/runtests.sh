#!/bin/bash
set -ex

# Create a temporary virtualenv to install fig
TDIR=`mktemp -d`
virtualenv $TDIR
. $TDIR/bin/activate
pip install fig

# Run Tests
fig --project-name jenkins${JOB_NAME}${BUILD_NUMBER} run -T web bin/unit_tests

# Delete virtualenv
rm -rf $TDIR
