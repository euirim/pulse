#!/bin/bash

pipenv install

# Apply migrations
pipenv run python manage.py migrate

# Add/update keyphrases (does no delete)
pipenv run python manage.py add_keyphrases data/keyphrases/2020_national_candidates.json

pipenv run gunicorn config.wsgi:application -w 2 -b :8000 --daemon

# start cron
/usr/bin/crontab crontab.txt
/usr/sbin/crond -f -l 8