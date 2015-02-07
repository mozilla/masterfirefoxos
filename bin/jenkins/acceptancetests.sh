#!/bin/bash
set -ex

COMMIT="${ghprbActualCommit:=$GIT_COMMIT}"

docker run $DOCKER_REPOSITORY:$COMMIT sh -c \
"DATABASE_URL=sqlite:// DEBUG=False ALLOWED_HOSTS=localhost SECRET_KEY=test \
PYTHONDONTWRITEBYTECODE=1 py.test --acceptance --baseurl=$BASE_URL -n $NUM_PROCS"
