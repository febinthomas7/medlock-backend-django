from django.db import models
from core.models import TimeStampedModel
from .claims import Claim

class ClaimDiagnosis(TimeStampedModel):
    class Meta:
        app_label = 'claim'
    claim = models.ForeignKey(Claim, on_delete=models.CASCADE)
    icd_code = models.CharField(max_length=20)
    description = models.TextField()
    priority = models.CharField(max_length=50, default='Medium')
    billing_diag_type = models.CharField(max_length=50, null=True, blank=True)
    service_type = models.CharField(max_length=20, null=True, blank=True)
    room_type = models.CharField(max_length=50, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

class ClaimProcedure(TimeStampedModel):
    class Meta:
        app_label = 'claim'
    claim = models.ForeignKey(Claim, on_delete=models.CASCADE)
    procedure_code = models.CharField(max_length=50)
    description = models.TextField()
    priority = models.CharField(max_length=50, default='Routine')
    billing_type = models.CharField(max_length=50, null=True, blank=True)
    start_datetime = models.DateTimeField(null=True, blank=True)
    end_datetime = models.DateTimeField(null=True, blank=True)
    sac_code = models.CharField(max_length=20, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

class ClaimLabOrder(TimeStampedModel):
    class Meta:
        app_label = 'claim'
    claim = models.ForeignKey(Claim, on_delete=models.CASCADE)
    loinc_code = models.CharField(max_length=50)
    description = models.TextField()
    sac_code = models.CharField(max_length=20, null=True, blank=True)
    quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    time_of_collection = models.DateTimeField(null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

class ClaimPrescription(TimeStampedModel):
    class Meta:
        app_label = 'claim'
    claim = models.ForeignKey(Claim, on_delete=models.CASCADE)
    drug_code = models.CharField(max_length=50)
    description = models.TextField()
    item_type = models.CharField(max_length=50)
    hsn_code = models.CharField(max_length=20, null=True, blank=True)
    quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    gst_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=12.00)
    added_at = models.DateTimeField(auto_now_add=True)