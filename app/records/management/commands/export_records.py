import datetime
import pytz
import json

from django.core.management.base import BaseCommand, CommandError
from django.core.serializers.json import DjangoJSONEncoder
from django.conf import settings
from django.db.models import F
from django.utils import timezone
from django.conf import settings

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

        # Make basetime midnight of the day of the earliest record
        # in the relevant time zone.
        my_tz = pytz.timezone(settings.TIME_ZONE)
        base_date = timezone.localtime(earliest_record.time_created).date()
        base_time = my_tz.localize(datetime.datetime(
            year=base_date.year,
            month=base_date.month,
            day=base_date.day,
        ))
        # Make now the midnight of the current day
        # in the relevant time zone.
        now_date = timezone.localtime(timezone.now()).date()
        now = my_tz.localize(datetime.datetime(
            year=now_date.year,
            month=now_date.month,
            day=now_date.day,
        ))

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
        while cur_time < now:
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

        # serialize
        result = []
        for row in output:
            record = {'Date': row[0].strftime('%m-%d-%Y')}
            for i in range(1, len(row)):
                record[header_row[i]] = row[i]

            result.append(record)

        # Save to disk
        with open(options['output_file'], 'w') as outfile:
            json.dump(
                result, 
                outfile,
                cls=DjangoJSONEncoder
            )

        self.stdout.write(
            self.style.SUCCESS(
                'Successfully exported records.'
            )
        )