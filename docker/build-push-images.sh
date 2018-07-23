#!/usr/bin/env bash

set -x

REPOSITORY=${REPOSITORY-debuhr}

docker-compose down
docker build -t ${REPOSITORY}/node-debug-chrome -f ./node-debug-chrome/Dockerfile . &&
docker build -t ${REPOSITORY}/node-debug-firefox -f ./node-debug-firefox/Dockerfile . &&
docker push ${REPOSITORY}/node-debug-chrome &&
docker push ${REPOSITORY}/node-debug-firefox
