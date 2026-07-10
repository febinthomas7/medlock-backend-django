from django.db import models
from core.models import TimeStampedModel
from claim.models.claims import Claim

class ClaimMlcDetail(models.Model):
    claim = models.OneToOneField(Claim, on_delete=models.CASCADE, primary_key=True)
    fir_number = models.CharField(max_length=100)
    police_station = models.CharField(max_length=150)
    cause_of_injury = models.CharField(max_length=255, null=True, blank=True)

class ClaimMaternityDetail(models.Model):
    claim = models.OneToOneField(Claim, on_delete=models.CASCADE, primary_key=True)
    delivery_date = models.DateField()
    delivery_type = models.CharField(max_length=50, default='Normal')
    living_children = models.IntegerField(default=0)

class ClaimDocument(TimeStampedModel):
    claim = models.ForeignKey(Claim, on_delete=models.CASCADE)
    uploaded_by_role = models.CharField(max_length=3)
    uploaded_by_id = models.BigIntegerField()
    document_type = models.CharField(max_length=50)
    document_mode = models.CharField(max_length=10, default='FILE')
    file_url = models.TextField(null=True, blank=True)
    file_size_kb = models.IntegerField(null=True, blank=True)
    document_text = models.TextField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class ClaimGovtPackage(TimeStampedModel):
    claim = models.ForeignKey(Claim, on_delete=models.CASCADE)
    package_code = models.CharField(max_length=50)
    package_name = models.CharField(max_length=150)
    category = models.CharField(max_length=100, null=True, blank=True)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    mapped_at = models.DateTimeField(auto_now_add=True)