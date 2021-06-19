#!/bin/bash

function print_help {
    echo -e "USAGE:\n\t$0 [-d delete_database] [-h help]"
    exit 0
}

while getopts ':hd' ARG; do
    case ${ARG} in
        h)
            print_help
            ;;
        d)
            PRUNE_DB=true
            ;;
    esac
done

docker container ls -a | grep -o "ratch_.*" | xargs docker container rm
docker network ls | grep -o "ratch_.*" | xargs docker network rm 

if [[ ! -z ${PRUNE_DB} ]]; then
    docker volume rm ratch_db_data
fi

docker compose up --build
