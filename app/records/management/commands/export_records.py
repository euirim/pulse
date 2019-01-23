import datetime

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db.models import F

import pandas as pd

from records.models import Record
from keyphrases.models import Keyphrase

class Command(BaseCommand):
    help = (
        'Exports records in database into a single csv file, ' + 
        'with all data for each keyphrase by date.'
    )

    def add_arguments(self, parser):
        parser.add_argument('output_file', type=str)

    def handle(self, *args, **options):
        Record.objects.annotate(
            adj_time_created=(
                F('time_created') - datetime.timedelta(minutes=1)
            )
        )
        pass