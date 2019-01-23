#!/bin/bash

# Add/update keyphrases (does no delete)
python manage.py add_keyphrases data/2020_national_candidates.json

# start cron
/usr/sbin/crond -f -l 8