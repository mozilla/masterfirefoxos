#!/bin/bash
# Needs DOCKER_USERNAME, DOCKER_PASSWORD, DOCKER_REPOSITORY
# environment variables.
#
# To set them go to Job -> Configure -> Build Environment -> Inject
# passwords and Inject env variables
#
set -ex

docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD -e $DOCKER_USERNAME@example.com

# Tag using git hash
docker tag -f `echo jenkins${JOB_NAME}${BUILD_NUMBER}_web | sed s/_//` $DOCKER_REPOSITORY:$GIT_COMMIT
docker push $DOCKER_REPOSITORY:$GIT_COMMIT

# Tag as latest
docker tag -f `echo jenkins${JOB_NAME}${BUILD_NUMBER}_web | sed s/_//` $DOCKER_REPOSITORY:latest
docker push $DOCKER_REPOSITORY:latest
