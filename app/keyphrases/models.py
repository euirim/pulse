from django.db import models

from utils.models import TimedModel

# Create your models here.
class Keyphrase(TimedModel):
    name = models.CharField(max_length=255)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name