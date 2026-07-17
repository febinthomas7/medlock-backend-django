from django.db import models
from core.models import CustomIDModel, TimeStampedModel
from apps.saas_core_admin.models.admins_hospitals import Hospital
from apps.common.exceptions import InvalidDepartmentWardError
from apps.common.constants import STANDARD_DEPARTMENT_TYPE



class Department(CustomIDModel):
    class Meta:
        app_label = 'hr_attendance_department'
        constraints = [
            models.UniqueConstraint(
                fields=['hospital', 'associated_plugin'], 
                name='unique_plugin_department_per_hospital',
                condition=models.Q(associated_plugin__isnull=False)
            )
        ]

    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=128)
    building_id = models.CharField(max_length=50, null=True, blank=True)
    floor = models.CharField(max_length=20, null=True, blank=True)
    associated_plugin = models.ForeignKey('plugin_rbac.Plugin', on_delete=models.RESTRICT, null=True, blank=True)
    department_type = models.CharField(max_length=20, default='DP')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Ward(CustomIDModel):

    class Meta:
        app_label = 'hr_attendance_department'

    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)

    def clean(self):
        # Wards can ONLY be created in standard clinical departments
        if self.department.department_type != STANDARD_DEPARTMENT_TYPE:
            # Call our centralized exception
            raise InvalidDepartmentWardError(
                department_name=self.department.name,
                required_type=STANDARD_DEPARTMENT_TYPE
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name



class Room(CustomIDModel):
    class Meta:
        app_label = 'hr_attendance_department'

    ward = models.ForeignKey(Ward, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=20)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)

class Bed(TimeStampedModel):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    bed_identifier = models.CharField(max_length=20)