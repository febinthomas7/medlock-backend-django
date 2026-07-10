from django.db import models
from core.models import TimeStampedModel
from saas_core_admin.models.admins_hospitals import Hospital
from user.models.personal import User
from user.models.medical import UserAppointment
from hr_attendance_department.models.hrs import Doctor
from claim.models.provider import InsuranceProvider, TpaProvider

class Claim(TimeStampedModel):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    appointment = models.ForeignKey(UserAppointment, on_delete=models.SET_NULL, null=True, blank=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True)
    
    plan_type = models.CharField(max_length=50, default='Retail')
    provider = models.ForeignKey(InsuranceProvider, on_delete=models.SET_NULL, null=True, blank=True)
    is_routed_via_tpa = models.BooleanField(default=False)
    tpa = models.ForeignKey(TpaProvider, on_delete=models.SET_NULL, null=True, blank=True)
    
    policy_number = models.CharField(max_length=100, null=True, blank=True)
    employee_id = models.CharField(max_length=100, null=True, blank=True)
    relationship_to_subscriber = models.CharField(max_length=50, default='Self')
    subscriber_name = models.CharField(max_length=150, null=True, blank=True)
    subscriber_govt_id = models.CharField(max_length=50, null=True, blank=True)
    
    clinical_notes = models.TextField(null=True, blank=True)
    necessity_justification = models.TextField(null=True, blank=True)
    patient_identity_verified_at = models.DateTimeField(null=True, blank=True)
    
    discharge_type = models.CharField(max_length=50, default='Routine')
    is_mlc = models.BooleanField(default=False)
    is_maternity = models.BooleanField(default=False)
    
    nhcx_claim_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    clinical_status = models.CharField(max_length=50, default='Draft')
    adminal_status = models.CharField(max_length=50, default='Pending Bill')
    claim_status = models.CharField(max_length=50, null=True, blank=True)
    auditor_query_note = models.TextField(null=True, blank=True)
    
    invoice_number = models.CharField(max_length=100, unique=True, null=True, blank=True)
    total_cgst = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_sgst = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    invoice_generated_at = models.DateTimeField(null=True, blank=True)
    total_billed_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    approved_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    clinical_payload = models.JSONField(null=True, blank=True)
    admin_payload = models.JSONField(null=True, blank=True)
    lifecycle_timeline = models.JSONField(null=True, blank=True)