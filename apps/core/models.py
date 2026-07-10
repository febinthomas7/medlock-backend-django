import uuid
from django.db import models

class CustomIDModel(models.Model):
    """
    Abstract model that replaces the default auto-incrementing ID with a 
    12-digit BigIntegerField starting at 190080070011.
    """
    id = models.BigIntegerField(primary_key=True, editable=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.id:
            last_record = self.__class__.objects.order_by('-id').first()
            if last_record:
                self.id = last_record.id + 1
            else:
                self.id = 190080070011
        super().save(*args, **kwargs)

class TimeStampedModel(models.Model):
    """
    Abstract base class providing a secure UUID primary key, 
    automatic creation/modification timestamps, and soft-delete support.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True