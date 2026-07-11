from django.db import models
from core.models import TimeStampedModel

class User(TimeStampedModel):
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A Positive'), ('A-', 'A Negative'),
        ('B+', 'B Positive'), ('B-', 'B Negative'),
        ('O+', 'O Positive'), ('O-', 'O Negative'),
        ('AB+', 'AB Positive'), ('AB-', 'AB Negative'),
        ('hh', 'Bombay Phenotype (hh)'),
        ('INRA', 'INRA (Indian Rare)'),
        ('OTHER', 'Other Rare Type'),
        ('UNKNOWN', 'Unknown / Pending Test'),
    ]
     
    name = models.CharField(max_length=150)
    password = models.CharField(max_length=128)
    contact = models.CharField(max_length=15, unique=True, null=True, blank=True)
    gmail = models.EmailField(max_length=100, null=True, blank=True)
    adhaar = models.CharField(max_length=20, unique=True, null=True, blank=True)
    abha = models.CharField(max_length=20, unique=True, null=True, blank=True)
    
    dob = models.DateField(null=True, blank=True)
    
    # User-reported (unverified) by default
    blood_group = models.CharField(max_length=10, choices=BLOOD_GROUP_CHOICES, default='UNKNOWN')
    
    # THE LOCK: Once True, the user cannot change their blood group via the app
    is_blood_group_verified = models.BooleanField(default=False) 

    class Meta:
        app_label = 'user'

    def __str__(self):
        return self.name

class EmergencyContact(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='emergency_contacts')
    name = models.CharField(max_length=150)
    relation = models.CharField(max_length=50)  # e.g., 'Spouse', 'Father', 'Friend'
    contact_number = models.CharField(max_length=15)
    is_primary = models.BooleanField(default=False)

    class Meta:
        app_label = 'user'  # <-- ADDED THIS HERE

    def __str__(self):
        return f"{self.name} ({self.relation})"