#!/bin/bash
#

for ((i=0; i<=500; i++)); do
    python marvin.py >>log/marvin.log 2>&1
    sleep 1
done

echo "Exceeded loop count" >>log/marvin.log
exit 1
