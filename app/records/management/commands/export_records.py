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
        'with all data for each keyphrase by date. Only looks at ' +
        'Twitter status count data.'
    )

    def add_arguments(self, parser):
        parser.add_argument('output_file', type=str)

    def handle(self, *args, **options):
        # identify base date
        earliest_record = Record.objects.earliest('time_created')

        base_time = earliest_record.time_created
        base_time.hour = 0
        base_time.minute = 0
        base_time.second = 0
        base_time.microsecond = 0

        records = Record.objects.annotate(
            # in case of leap seconds (which may add an additional interval)
            adj_time_created=(
                F('time_created') + datetime.timedelta(seconds=2)
            )
        )

        # Get all display=True keyphrases
        keyphrases = Keyphrase.objects.filter(display=True).order_by('name')
        header_row = ['Date'] + [k.name for k in keyphrases]

        result = []
        cur_time = base_time
        while cur_time < datetime.timezone.now():
            records = Record.objects.filter(
                time_created__gte=cur_time,
                time_created__lt=cur_time + datetime.timedelta(day=1)
            )
            result = [0] * len(keyphrases)

            for record in records:
                kps = record.payload['keyphrases']
                for i, k in enumerate(keyphrases):
                    if k.name in kps:
                        tweet_count = kps[k.name]['twitter']['tweet_count']
                        result[i] += tweet_count

            result.append([cur_time] + result)
            
            cur_time += datetime.timedelta(day=1)

        # Convert to dataframe
        df = pd.DataFrame.from_records(result, columns=header_row)

        # Save to disk
        df.to_csv(options['output_file'], index=False)