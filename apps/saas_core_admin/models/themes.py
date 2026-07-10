from django.db import models
from core.models import TimeStampedModel

class Theme(TimeStampedModel):
    name = models.CharField(max_length=100)
    primary = models.CharField(max_length=7, null=True, blank=True)
    secondary = models.CharField(max_length=7, null=True, blank=True)

    def __str__(self):
        return self.name