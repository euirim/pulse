from django.db import models
from django.contrib.postgres.fields import ArrayField

from utils.models import TimedModel

# Create your models here.
class Keyphrase(TimedModel):
    name = models.CharField(max_length=255, unique=True)
    aliases = ArrayField(
        models.CharField(max_length=255), 
        blank=True, 
        null=True
    )
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name