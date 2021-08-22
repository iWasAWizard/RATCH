#!/bin/bash

function print_help {
echo -e """
USAGE:\n    $0 [ -sd ] [ -h ]
\t-r: Re-build Docker containers.
\t-d: [DANGEROUS] Delete and recreate the database volume, erasing all current data.
\t-h: Print this help text.
"""
    exit 0
}

function clean_app_instance {
    echo '[*] Cleaning up Docker environment!'
    docker-compose down

    if [[ -n ${PRUNE_DB} ]]; then
        echo '[*] Removing database volume!'
        docker volume rm ratch_db_data
    fi
}

while getopts ':hdr' ARG; do
    case ${ARG} in
        h)
            print_help
            ;;
        d)
            PRUNE_DB=true
            ;;
        r)
            AUTOSTART_NEW_INSTANCE=true
            ;;
        *)
            print_help
            ;;
    esac
done

if [[ -n ${AUTOSTART_NEW_INSTANCE} ]]; then
    clean_app_instance
elif [[ -n $(docker container ls -a | grep -o 'ratch') ]]; then
    echo '[*] RATCH containers currently exist!'
    read -p '[*] Remove existing RATCH instance? [y/n] ' -r

    while [[ ! ${REPLY} =~ ^[yYnN]$ ]]; do
        read -p "[*] Invalid input. Do you want to remove the existing RATCH instance? [y/n] " -r
    done

    if [[ $REPLY =~ ^[Nn]$ ]]; then
        echo '[*] Containers intact! Stopping initialization...'
        exit 1
    else
        clean_app_instance
    fi
fi

docker compose up --build
