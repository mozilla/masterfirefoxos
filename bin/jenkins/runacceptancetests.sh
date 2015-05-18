#!/bin/bash
#
# Runs acceptance tests.
#
# Needs DOCKER_REPOSITORY, BASE_URL and optionally NUM_PROCS
#
# To set them go to Job -> Configure -> Build Environment -> Inject
# passwords and Inject env variables
#
set -ex

REVISION=$(curl $BASE_URL/static/revision.txt)
echo REVISION=$REVISION
ENV_FILE=`mktemp`
echo "DATABASE_URL=sqlite://" >> $ENV_FILE
echo "DEBUG=False" >> $ENV_FILE
echo "ALLOWED_HOSTS=localhost" >> $ENV_FILE
echo "SECRET_KEY=test" >> $ENV_FILE

# Run Tests
docker run --env-file=$ENV_FILE $DOCKER_REPOSITORY:$REVISION py.test -m acceptance --acceptance --baseurl=$BASE_URL -n ${NUM_PROCS:-7}

# Delete temp file.
rm -rf $ENV_FILE
