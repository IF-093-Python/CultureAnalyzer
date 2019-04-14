#!/usr/bin/env bash

export DOCKER_ENABLE=True

./scripts/wait-for-it.sh ${PG_HOST}:${PG_PORT_IN} -s -t 40 -- ./scripts/bind-gunicorn.sh