from django.db import models
from core.models import CustomIDModel
from .departments import Department
from apps.common.constants import STANDARD_DEPARTMENT_TYPE, PLUGIN_DEPARTMENT_CONFIG

class Doctor(CustomIDModel):
    class Meta:
        app_label = 'hr_attendance_department'

    name = models.CharField(max_length=150)
    password = models.CharField(max_length=128)
    adhaar = models.CharField(max_length=20, unique=True, null=True, blank=True)
    contact = models.CharField(max_length=15, null=True, blank=True)
    gmail = models.EmailField(max_length=100, unique=True, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    punch_id = models.IntegerField()
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    designation = models.CharField(max_length=100, null=True, blank=True)
    staff_type = models.CharField(max_length=3, default='DR')
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # Enforce strict staff role assignment based on the Department type
        dept_type = self.department.department_type

        if dept_type != STANDARD_DEPARTMENT_TYPE:
            # Look up the strict role in the rulebook
            config = PLUGIN_DEPARTMENT_CONFIG.get(dept_type)
            if config:
                # Force the staff_type to match the isolated wing (e.g., 'BD' for Blood Bank)
                self.staff_type = config['roles']['Doctor']
        else:
            # Standard clinical doctor
            self.staff_type = 'DR'

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name



class Nurse(CustomIDModel):
    class Meta:
        app_label = 'hr_attendance_department'

    name = models.CharField(max_length=150)
    password = models.CharField(max_length=128)
    adhaar = models.CharField(max_length=20, unique=True, null=True, blank=True)
    contact = models.CharField(max_length=15, null=True, blank=True)
    gmail = models.EmailField(max_length=100, unique=True, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    punch_id = models.IntegerField()
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    staff_type = models.CharField(max_length=3, default='NS')
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # Enforce strict staff role assignment based on the Department type
        dept_type = self.department.department_type

        if dept_type != STANDARD_DEPARTMENT_TYPE:
            # Look up the strict role in the rulebook
            config = PLUGIN_DEPARTMENT_CONFIG.get(dept_type)
            if config:
                # Force the staff_type to match the isolated wing (e.g., 'BN' for Blood Bank)
                self.staff_type = config['roles']['Nurse']
        else:
            # Standard clinical nurse
            self.staff_type = 'NS'

        super().save(*args, **kwargs)



class Receptionist(CustomIDModel):
    class Meta:
        app_label = 'hr_attendance_department'

    name = models.CharField(max_length=150)
    password = models.CharField(max_length=128)
    adhaar = models.CharField(max_length=20, unique=True, null=True, blank=True)
    contact = models.CharField(max_length=15, null=True, blank=True)
    gmail = models.EmailField(max_length=100, unique=True, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    punch_id = models.IntegerField()
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    staff_type = models.CharField(max_length=3, default='RS')
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # Enforce strict staff role assignment based on the Department type
        dept_type = self.department.department_type

        if dept_type != STANDARD_DEPARTMENT_TYPE:
            # Look up the strict role in the rulebook
            config = PLUGIN_DEPARTMENT_CONFIG.get(dept_type)
            if config:
                # Force the staff_type to match the isolated wing (e.g., 'BR' for Blood Bank)
                self.staff_type = config['roles']['Receptionist']
        else:
            # Standard clinical receptionist
            self.staff_type = 'RS'

        super().save(*args, **kwargs)
