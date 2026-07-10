from django.db import models
from core.models import TimeStampedModel
from saas_core_admin.models.admins_hospitals import Hospital
from hr_attendance_department.models.departments import Department

class BiometricPunch(TimeStampedModel):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    device_ip = models.CharField(max_length=50, null=True, blank=True)
    punch_id = models.IntegerField()
    punch_time = models.DateTimeField(auto_now_add=True)
    punch_type = models.CharField(max_length=10, null=True, blank=True)

class StaffAttendance(TimeStampedModel):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    staff_role = models.CharField(max_length=3)
    staff_id = models.BigIntegerField()
    date = models.DateField(auto_now_add=True)
    check_in_time = models.DateTimeField(null=True, blank=True)
    check_out_time = models.DateTimeField(null=True, blank=True)
    total_hours = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, default='Present')

    class Meta:
        unique_together = ('staff_id', 'date')