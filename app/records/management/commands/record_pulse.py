from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from records.models import Record
from keyphrases.models import Keyphrase
from core.pulse import KeyphraseRecordPool

class Command(BaseCommand):
    help = (
        'Checks the global traction of active keyphrases and ' + 
        'creates relevant records.'
    )

    def handle(self, *args, **options):
        keyphrase_objects = Keyphrase.objects.filter(active=True)
        if len(keyphrase_objects) == 0:
            raise CommandError('No keyphrases in database.')
        elif len(keyphrase_objects) > 100:
            raise CommandError('More keyphrases than safe for API.')

        keyphrases = [
            (k.name, k.aliases)
            if k.aliases else (k.name, [])
            for k in keyphrase_objects
        ]

        pool = KeyphraseRecordPool(
            collection_interval=settings.PULSE_CHECK_FREQUENCY
        )
        pool.fill(keyphrases)
        for record in pool.keyphrase_records:
            keyphrase = Keyphrase.objects.get(name__iexact=record.keyphrase)
            Record.objects.create(
                keyphrase=keyphrase,
                payload=record.serialize_payload()
            ) 

        self.stdout.write(
            self.style.SUCCESS(
                'Successfully created records.'
            )
        )