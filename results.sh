#!/usr/bin/env bash
cd /home/tensorcat/projects/bots/fedibot/fedibot/
/usr/bin/python results.py 2>&1 > results/$(/usr/bin/date +%Y%m%d%H%M%S)results.csv