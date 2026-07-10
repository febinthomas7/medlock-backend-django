from django.db import models
from core.models import CustomIDModel
from saas_core_admin.models.subscriptions import Subscription
from saas_core_admin.models.themes import Theme

class Admin(CustomIDModel):
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
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    password = models.CharField(max_length=128)
    location = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name