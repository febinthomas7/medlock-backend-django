from django.db import models
from core.models import CustomIDModel
from .subscriptions import Subscription
from .themes import Theme

class Admin(CustomIDModel):
    class Meta:
        app_label = 'saas_core_admin'

    name = models.CharField(max_length=150)
    password = models.CharField(max_length=128)
    contact = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(max_length=100, unique=True, null=True, blank=True)
    theme = models.ForeignKey(Theme, on_delete=models.SET_NULL, null=True, blank=True)
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Hospital(CustomIDModel):
    class Meta:
        app_label = 'saas_core_admin'

    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    password = models.CharField(max_length=128)
    location = models.TextField(null=True, blank=True)
    # Add these missing fields to match the frontend:
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    npi_id = models.CharField(max_length=100, blank=True, null=True)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    image_url = models.URLField(max_length=1000, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name