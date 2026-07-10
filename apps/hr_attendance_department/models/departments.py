from django.db import models
from core.models import CustomIDModel, TimeStampedModel
from saas_core_admin.models.admins_hospitals import Hospital

class Department(CustomIDModel):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=128)
    building_id = models.CharField(max_length=50, null=True, blank=True)
    floor = models.CharField(max_length=20, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Ward(CustomIDModel):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Room(CustomIDModel):
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=20)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)

class Bed(TimeStampedModel):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    bed_identifier = models.CharField(max_length=20)