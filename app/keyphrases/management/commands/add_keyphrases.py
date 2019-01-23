import json

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from keyphrases.models import Keyphrase

class Command(BaseCommand):
    help = (
        'Adds non-redundant keyphrases from a given file ' + 
        'to the database.'
    )

    def add_arguments(self, parser):
        parser.add_argument('keyphrase_file', type=str)

    def handle(self, *args, **options):
        # load file and read JSON
        try:
            json_data = open(options['keyphrase_file']).read()
        except:
            raise CommandError('Failed to open keyphrase file.')

        keyphrases = json.loads(json_data)

        for kp in keyphrases:
            # check if keyphrase is already entered
            try:
                keyphrase = Keyphrase.objects.get(name=kp['name'])
                # add aliases
                keyphrase.update(aliases=kp['aliases'])
            except Keyphrase.DoesNotExist:
                # create keyphrase
                Keyphrase.objects.create(
                    name=kp['name'],
                    aliases=kp['aliases'],
                    active=True
                )

        self.stdout.write(
            self.style.SUCCESS(
                'Successfully added/updated keyphrases.'
            )
        )