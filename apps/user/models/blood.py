from django.db import models
from core.models import TimeStampedModel
from user.models.personal import User
from saas_core_admin.models.admins_hospitals import Hospital
from hr_attendance_department.models.hrs import Nurse

class UserBloodAppointment(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    scheduled_at = models.DateTimeField()
    status = models.CharField(max_length=50, default='PENDING')

class UserBloodDonation(TimeStampedModel):
    COMPONENT_CHOICES = [
        ('RBC', 'Red Blood Cells'),
        ('PLATELETS', 'Platelets'),
        ('PLASMA', 'Plasma')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    nurse = models.ForeignKey(Nurse, on_delete=models.SET_NULL, null=True, blank=True)
    blood_group = models.CharField(max_length=10) # Made max_length=10 to match User model
    quantity_ml = models.IntegerField(default=450)
    component_type = models.CharField(max_length=20, choices=COMPONENT_CHOICES, default='RBC')
    donation_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # 1. Check if a valid, accurate blood group is being saved
        if self.blood_group and self.blood_group != 'UNKNOWN':
            
            # 2. Update the parent User's profile with the accurate data
            self.user.blood_group = self.blood_group
            
            # 3. Trigger the Lock
            self.user.is_blood_group_verified = True
            
            # 4. Save the parent User (update_fields makes the database query extremely fast)
            self.user.save(update_fields=['blood_group', 'is_blood_group_verified'])
            
        # 5. Continue saving this specific Blood Donation record normally
        super().save(*args, **kwargs)