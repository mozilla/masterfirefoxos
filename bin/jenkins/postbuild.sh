#!/bin/bash
set -ex

# Fig does not remove the running database instace. We cannot use fig
# rm here because we re-tagged the image while uploading to DockerHub.
docker rm -f `echo jenkins${JOB_NAME}${BUILD_NUMBER}| sed s/_//g`_db_1
