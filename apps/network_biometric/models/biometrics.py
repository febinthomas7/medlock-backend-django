from django.db import models
from django.db.models import Q
from core.models import TimeStampedModel

class BiometricDeviceMapping(TimeStampedModel):
    device_ip = models.CharField(max_length=50)
    punch_id = models.IntegerField()
    staff_role = models.CharField(max_length=3)
    staff_id = models.BigIntegerField()
    is_currently_assigned = models.BooleanField(default=True)
    assigned_at = models.DateTimeField(auto_now_add=True)
    unassigned_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        app_label = 'network_biometric'
        constraints = [
            models.UniqueConstraint(
                fields=['device_ip', 'punch_id'],
                condition=Q(is_currently_assigned=True),
                name='idx_unique_active_punch'
            )
        ]