#!/usr/bin/env bash
cd /home/tensorcat/projects/bots/fedibot/fedibot/
/usr/bin/python results.py 2>&1 >> files/logs/results.logs
rsync results/* tensorcat@tensorcat.com:results/