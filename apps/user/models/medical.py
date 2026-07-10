from django.db import models
from core.models import TimeStampedModel
from user.models.personal import User
from saas_core_admin.models.admins_hospitals import Hospital
from hr_attendance_department.models.hrs import Doctor
from hr_attendance_department.models.departments import Department

class UserAppointment(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    scheduled_at = models.DateTimeField()
    status = models.CharField(max_length=50, default='SCHEDULED')

class UserReport(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True)
    report_type = models.CharField(max_length=100, null=True, blank=True)
    report_payload = models.JSONField(null=True, blank=True)
    generated_at = models.DateTimeField(auto_now_add=True)

class UserEvent(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=100)
    event_description = models.TextField(null=True, blank=True)
    event_time = models.DateTimeField(auto_now_add=True)