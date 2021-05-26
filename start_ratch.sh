#!/bin/bash

docker container ls -aq | xargs docker container stop
docker container ls -aq | xargs docker container rm
docker volume prune -f

docker-compose up --build
