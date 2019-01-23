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

        # Create record to make sure you record time before recording data.
        new_record = Record.objects.create(
            payload={},
            interval=settings.PULSE_CHECK_FREQUENCY
        )

        pool = KeyphraseRecordPool(
            collection_interval=settings.PULSE_CHECK_FREQUENCY
        )
        pool.fill(keyphrases)

        total_tweet_count = 0
        payload_keyphrases = {}
        for record in pool.keyphrase_records:
            try:
                keyphrase = Keyphrase.objects.get(
                    name__iexact=record.keyphrase, 
                    active=True
                )
            except Keyphrase.DoesNotExist:
                continue

            total_tweet_count += record.twitter.tweet_count
            payload_keyphrases[keyphrase.name] = record.serialize_payload()

        payload = {
            'keyphrases': payload_keyphrases, 
            'total_tweet_count': total_tweet_count    
        }

        new_record.payload = payload
        new_record.save()

        self.stdout.write(
            self.style.SUCCESS(
                'Successfully created records.'
            )
        )