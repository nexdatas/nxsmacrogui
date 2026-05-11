#!/usr/bin/env bash

if [[ $1 == "2" ]]; then
    echo "run nxstaurusgui"
    docker exec  ndts python test
else
    echo "run nxstaurusgui3"
    docker exec  ndts python3 test
fi
ERR=$?

echo "ERROR: "$ERR

if [ $ERR != 0 ]; then
    if [ $ERR != 139 ]; then
	exit $ERR;
    fi
fi
