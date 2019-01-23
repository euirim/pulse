import datetime
import pytz

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db.models import F
from django.utils import timezone
from django.conf import settings

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

        base_time = datetime.datetime(
            year=earliest_record.time_created.year,
            month=earliest_record.time_created.month,
            day=earliest_record.time_created.day,
            tzinfo=pytz.timezone(settings.TIME_ZONE)
        )

        print(base_time)

        records = Record.objects.annotate(
            # in case of leap seconds (which may add an additional interval)
            adj_time_created=(
                F('time_created') + datetime.timedelta(seconds=2)
            )
        )

        # Get all display=True keyphrases
        keyphrases = Keyphrase.objects.filter(display=True).order_by('name')
        header_row = ['Date'] + [k.name for k in keyphrases]

        output = []
        cur_time = base_time
        now = timezone.now()
        while cur_time.day < now.day:
            records = Record.objects.filter(
                time_created__gte=cur_time,
                time_created__lt=cur_time + datetime.timedelta(days=1)
            )
            result = [0] * len(keyphrases)

            for record in records:
                # To catch record in the process of being created
                if 'keyphrases' not in record.payload:
                    continue

                kps = record.payload['keyphrases']
                for i, k in enumerate(keyphrases):
                    if k.name in kps:
                        tweet_count = kps[k.name]['twitter']['tweet_count']
                        result[i] += tweet_count

            output.append([cur_time.replace(tzinfo=None)] + result)
            
            cur_time += datetime.timedelta(days=1)

        # Convert to dataframe
        df = pd.DataFrame.from_records(output, columns=header_row)

        # Save to disk
        df.to_csv(options['output_file'], index=False)

        self.stdout.write(
            self.style.SUCCESS(
                'Successfully exported records.'
            )
        )