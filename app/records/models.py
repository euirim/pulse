from django.db import models
from django.contrib.postgres.fields import JSONField

from utils.models import TimedModel
from keyphrases.models import Keyphrase

# Create your models here.
class Record(TimedModel):
    keyphrase = models.ForeignKey(
        Keyphrase,
        db_index=True,
        on_delete=models.PROTECT
    )
    data = JSONField()

    def __str__(self):
        return '{0} {1}'.format(
            self.keyphrase.name, 
            self.time_created
        )