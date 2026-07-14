from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
import re

from apps.saas_core_admin.models.admins_hospitals import Admin, Hospital
from apps.hr_attendance_department.models.departments import Department, Ward, Room
from apps.hr_attendance_department.models.hrs import Doctor, Nurse, Receptionist

class RoleBasedLoginView(APIView):
    """
    Handles POST requests to /api/<role>/login/ using Custom 12-digit IDs
    """
    permission_classes = [] 
    authentication_classes = []

    # Map URL roles/prefixes to their exact Django Model
    ROLE_MODEL_MAP = {
        "admin": Admin, "ad": Admin,
        "hospital": Hospital, "hp": Hospital,
        "department": Department, "dp": Department,
        "ward": Ward, "wr": Ward,
        "room": Room, "rm": Room,
        "doctor": Doctor, "dr": Doctor,
        "nurse": Nurse, "ns": Nurse,
        "receptionist": Receptionist, "rs": Receptionist
    }

    def post(self, request, role):
        # 1. Get the ID and password from the request
        provided_id = request.data.get("id") or request.data.get("username")
        password = request.data.get("password")

        if not provided_id or not password:
            return Response(
                {"error": "Please provide both id and password."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 2. Clean the ID: Strip out "Ad-", "Dr-", etc.
        numeric_id_str = re.sub(r'\D', '', str(provided_id))
        
        if not numeric_id_str:
            return Response(
                {"error": "Invalid ID format. Must contain the 12-digit number."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        numeric_id = int(numeric_id_str)
        role = role.lower()

        # 3. Look up the Model based on the role dictionary
        ModelClass = self.ROLE_MODEL_MAP.get(role)
        
        if not ModelClass:
            return Response({"error": "Invalid login role."}, status=status.HTTP_400_BAD_REQUEST)

        # Automatically derive the standard role name (e.g., 'Admin' -> 'admin')
        role_name = ModelClass.__name__.lower()

        # 4. Query the exact custom table using the designated Model
        try:
            user_instance = ModelClass.objects.get(id=numeric_id)
        except ModelClass.DoesNotExist:
            return Response({"error": "User with this ID not found."}, status=status.HTTP_404_NOT_FOUND)

        # 5. Verify the password (TODO: implement password hashing checks)
        if user_instance.password != password:
            return Response(
                {"error": "Invalid password."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # 6. Prepare Theme Data
        theme_data = None
        if hasattr(user_instance, 'theme') and user_instance.theme:
            theme_data = {
                "primary": getattr(user_instance.theme, 'primary', getattr(user_instance.theme, 'primary_color', '#000000')),
                "secondary": getattr(user_instance.theme, 'secondary', getattr(user_instance.theme, 'secondary_color', '#FFFFFF')),
                "mode": getattr(user_instance.theme, 'mode', 'light')
            }

        # 7 Generate Custom JWT Token
        refresh = RefreshToken()
        refresh['user_id'] = user_instance.id
        refresh['role'] = role_name
        

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "role": role_name,
            "user_id": getattr(user_instance, 'custom_id', user_instance.id), # Fallback to id if custom_id field doesn't exist
            "name": getattr(user_instance, 'name', 'Unknown')
        }, status=status.HTTP_200_OK)