#!/usr/bin/env bash

export DOCKER_ENABLE=True

./scripts/wait-for-it.sh ${PG_HOST}:${PG_PORT_IN} -s -t 50 -- \
./scripts/wait-for-it.sh ${RD_HOST}:${RD_PORT_IN} -s -t 20 -- \
./scripts/bind-gunicorn.sh