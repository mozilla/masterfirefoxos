#!/bin/bash
#
# Runs unit_tests
#
set -ex

# Create a temporary virtualenv to install fig
TDIR=`mktemp -d`
virtualenv $TDIR
. $TDIR/bin/activate
pip install fig

FIG_CMD="fig --project-name jenkins${JOB_NAME}${BUILD_NUMBER} -f ./bin/jenkins/fig.yml"

$FIG_CMD run -T web flake8

# Lint translations
$FIG_CMD run -T web dennis-cmd lint --errorsonly locale/

# Run Tests
$FIG_CMD run -T web py.test --cov masterfirefoxos --cov-report=term-missing

# Delete virtualenv
rm -rf $TDIR
