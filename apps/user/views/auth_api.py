from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed

# Import your models exactly as you did in your view
from apps.saas_core_admin.models.admins_hospitals import Admin, Hospital
from apps.hr_attendance_department.models.departments import Department, Ward, Room
from apps.hr_attendance_department.models.hrs import Doctor, Nurse, Receptionist

class ERPJWTAuthentication(JWTAuthentication):
    ROLE_MODEL_MAP = {
        "admin": Admin,
        "hospital": Hospital,
        "department": Department,
        "ward": Ward,
        "room": Room,
        "doctor": Doctor,
        "nurse": Nurse,
        "receptionist": Receptionist
    }

    def get_user(self, validated_token):
        """
        Intercepts the token, reads the role, and queries the correct ERP table.
        """
        try:
            user_id = validated_token["user_id"]
            role = validated_token.get("role")
        except KeyError:
            raise AuthenticationFailed("Token contained no recognizable user identification")

        if not role or role not in self.ROLE_MODEL_MAP:
            raise AuthenticationFailed("Token contains invalid or missing role")

        # Select the correct database table based on the role
        ModelClass = self.ROLE_MODEL_MAP[role]

        try:
            user = ModelClass.objects.get(id=user_id)
        except ModelClass.DoesNotExist:
            raise AuthenticationFailed("User not found in role table", code="user_not_found")

        # DRF's IsAuthenticated permission checks if `user.is_authenticated` is True.
        # Since you are using custom models, we dynamically attach this property so DRF lets them pass.
        setattr(user, 'is_authenticated', True)
        
        return user