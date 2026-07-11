from django.db import models
from core.models import TimeStampedModel
from apps.saas_core_admin.models.admins_hospitals import Admin, Hospital

class HospitalNetwork(TimeStampedModel):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    cidr_block = models.CharField(max_length=50)
    network_name = models.CharField(max_length=100, null=True, blank=True)

class AdminNetwork(TimeStampedModel):
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)
    cidr_block = models.CharField(max_length=50)
    network_name = models.CharField(max_length=100, null=True, blank=True)