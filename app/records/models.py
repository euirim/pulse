from django.db import models
from django.contrib.postgres.fields import JSONField

from utils.models import TimedModel
from keyphrases.models import Keyphrase

# Create your models here.
class Record(TimedModel):
    payload = JSONField()
    interval = models.PositiveIntegerField(
        help_text=(
            'The number of seconds in which data ' + 
            'was recorded for this record.'
        )
    )

    def __str__(self):
        return '{}'.format(self.time_created)