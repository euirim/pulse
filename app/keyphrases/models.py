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
    active = models.BooleanField(
        default=True, 
        help_text="When checked, data is collected about this keyphrase."
    )
    display = models.BooleanField(
        default=False,
        help_text="When checked, data is included in API responses."
    )

    def __str__(self):
        return self.name