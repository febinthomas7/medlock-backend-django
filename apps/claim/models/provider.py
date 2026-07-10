from django.db import models
from core.models import TimeStampedModel

class TpaProvider(TimeStampedModel):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

class InsuranceProvider(TimeStampedModel):
    name = models.CharField(max_length=150)
    category = models.CharField(max_length=50, default='Retail')
    nhcx_routing_code = models.CharField(max_length=50, unique=True, null=True, blank=True)

    def __str__(self):
        return self.name