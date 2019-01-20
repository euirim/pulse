from django.db import models

# Create your models here.
class TimedModel(models.Model):
    time_created = models.DateTimeField(
        auto_now_add=True, 
        db_index=True
    )

    class Meta:
        abstract = True