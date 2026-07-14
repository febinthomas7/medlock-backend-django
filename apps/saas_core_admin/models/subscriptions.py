from django.db import models
from core.models import TimeStampedModel

class Subscription(TimeStampedModel):
    class Meta:
        app_label = 'saas_core_admin'

    tier_name = models.CharField(max_length=100, unique=True)
    max_branches = models.IntegerField()
    max_staffs = models.IntegerField()
    description = models.TextField(blank=True)
    price_monthly = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    price_annual = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    currency = models.CharField(max_length=3, default='INR')

    def __str__(self):
        return self.tier_name