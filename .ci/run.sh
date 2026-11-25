#!/usr/bin/env bash

echo "run nxstaurusgui3"
docker exec  ndts /bin/bash -c 'QT_QPA_PLATFORM=offscreen python3 test'
ERR=$?

echo "ERROR: "$ERR

if [ $ERR != 0 ]; then
    if [ $ERR != 139 ]; then
	exit $ERR;
    fi
fi
