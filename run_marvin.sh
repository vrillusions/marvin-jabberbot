#!/bin/bash
#
while [ true ]; do
	python marvin.py >>log/marvin.log 2>&1
	sleep 1
done
