from django.db import models
from core.models import CustomIDModel
from hr_attendance_department.models.departments import Department

class Doctor(CustomIDModel):
    name = models.CharField(max_length=150)
    password = models.CharField(max_length=128)
    adhaar = models.CharField(max_length=20, unique=True, null=True, blank=True)
    contact = models.CharField(max_length=15, null=True, blank=True)
    gmail = models.EmailField(max_length=100, unique=True, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    punch_id = models.IntegerField()
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    designation = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Nurse(CustomIDModel):
    name = models.CharField(max_length=150)
    password = models.CharField(max_length=128)
    adhaar = models.CharField(max_length=20, unique=True, null=True, blank=True)
    contact = models.CharField(max_length=15, null=True, blank=True)
    gmail = models.EmailField(max_length=100, unique=True, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    punch_id = models.IntegerField()
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)

class Receptionist(CustomIDModel):
    name = models.CharField(max_length=150)
    password = models.CharField(max_length=128)
    adhaar = models.CharField(max_length=20, unique=True, null=True, blank=True)
    contact = models.CharField(max_length=15, null=True, blank=True)
    gmail = models.EmailField(max_length=100, unique=True, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    punch_id = models.IntegerField()
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)