from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
import re
from django.apps import apps

# Import both mappings from your single source of truth
from apps.common.constants import ROLE_MODEL_MAP

class RoleBasedLoginView(APIView):
    """
    Handles POST requests to /api/<role>/login/ using Custom 12-digit IDs
    """
    permission_classes = [] 
    authentication_classes = []

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

        # 3. Get the string path from constants
        model_path = ROLE_MODEL_MAP.get(role)
        
        if not model_path:
            return Response({"error": "Invalid login role."}, status=status.HTTP_400_BAD_REQUEST)

        # 4. CONVERT THE STRING TO A REAL DJANGO MODEL
        try:
            ModelClass = apps.get_model(model_path)
        except LookupError:
            return Response({"error": "System configuration error. Model not found."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # -------------------------------------------------------------
        # 5. Build contextual database query (The Database Firewall)
        # -------------------------------------------------------------
        query_kwargs = {"id": numeric_id}
        model_name = ModelClass.__name__

        if model_name == 'Department':
            query_kwargs["department_type"] = role.upper()
            
        elif model_name in ['Doctor', 'Nurse', 'Receptionist']:
            query_kwargs["staff_type"] = role.upper()

        # Proceed with the database query normally
        try:
            # Fails immediately if the database type doesn't exactly match the URL role!
            user_instance = ModelClass.objects.get(**query_kwargs)
        except ModelClass.DoesNotExist:
            return Response({"error": "User not found or access denied for this portal."}, status=status.HTTP_404_NOT_FOUND)

        if user_instance.password != password:
            return Response({"error": "Invalid password."}, status=status.HTTP_401_UNAUTHORIZED)

        # 6. Now this will work perfectly because ModelClass is a real model!
        # Inject the plugin-specific role (e.g., 'id') if they are non-clinical, otherwise use generic (e.g., 'doctor')
        is_plugin = query_kwargs.get("department_type") not in [None, 'DP'] or query_kwargs.get("staff_type") not in [None, 'DP']
        role_name = role if is_plugin else model_name.lower()

        # 7. Prepare Theme Data
        theme_data = None
        if hasattr(user_instance, 'theme') and user_instance.theme:
            theme_data = {
                "primary": getattr(user_instance.theme, 'primary', getattr(user_instance.theme, 'primary_color', '#000000')),
                "secondary": getattr(user_instance.theme, 'secondary', getattr(user_instance.theme, 'secondary_color', '#FFFFFF')),
                "mode": getattr(user_instance.theme, 'mode', 'light')
            }

        # 8 Generate Custom JWT Token
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