#!/bin/bash

# Apply migrations
pipenv run python manage.py migrate

# Add/update keyphrases (does no delete)
pipenv run python manage.py add_keyphrases data/keyphrases/2020_national_candidates.json

# start cron
/usr/sbin/crond -f -l 8