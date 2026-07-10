from django.db import models
from core.models import TimeStampedModel

class Subscription(TimeStampedModel):
    tier_name = models.CharField(max_length=100, unique=True)
    max_branches = models.IntegerField()
    max_staffs = models.IntegerField()

    def __str__(self):
        return self.tier_name