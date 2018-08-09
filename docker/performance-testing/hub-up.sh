#!/usr/bin/env bash

display_usage() {
    echo "*** CUAHSI Performance Testing Control Script ***"
    echo "usage: $0 [firefox] [chrome]  # setup Selenium Grid with [firefox] firefox nodes and [chrome] chrome nodes"
}

# Display usage if less than 2 arguments provided
if [  $# -lt 2 ]
then
    display_usage
    exit 1
fi

# Start Selenium hub with specified number of Firefox and Chrome nodes
docker-compose up -d --scale firefox=$1 --scale chrome=$2
./hub-vnc-start.sh
