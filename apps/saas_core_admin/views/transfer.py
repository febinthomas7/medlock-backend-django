from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from apps.hr_attendance_department.models.departments import Department
from apps.saas_core_admin.services import transfer as services
from apps.plugin_rbac.permissions.navigation import HasRBACPermission

class StaffTransferView(APIView):
    permission_classes = [IsAuthenticated, HasRBACPermission]
    required_rbac_permission = "Staff Transfer"

    def post(self, request):
        """Transfer a staff member to a new department/hospital"""
        try:
            data = request.data
            role = data.get('role')
            staff_id = data.get('staff_id')
            new_department_id = data.get('new_department_id')

            if not role or not staff_id or not new_department_id:
                return Response({
                    "status": False, 
                    "message": "Role, Staff ID, and Target Department ID are required."
                }, status=status.HTTP_400_BAD_REQUEST)

            # Pass request down to the secure service layer
            staff_member, new_department = services.execute_staff_transfer(
                user=request.user,
                role=role,
                staff_id=staff_id,
                new_department_id=new_department_id
            )

            return Response({
                "status": True,
                "message": f"{role.capitalize()} successfully transferred to {new_department.name}."
            }, status=status.HTTP_200_OK)

        # --- ERROR HANDLING ---
        except Department.DoesNotExist:
            return Response({
                "status": False,
                "message": "Destination department not found or you lack permission to access it."
            }, status=status.HTTP_404_NOT_FOUND)
            
        except ObjectDoesNotExist:
            # This dynamically catches Doctor.DoesNotExist, Nurse.DoesNotExist, etc.
            return Response({
                "status": False,
                "message": "Staff member not found or you lack permission to modify them."
            }, status=status.HTTP_404_NOT_FOUND)
            
        except PermissionError as e:
            return Response({
                "status": False,
                "message": str(e)
            }, status=status.HTTP_403_FORBIDDEN)
            
        except ValueError as e:
            return Response({
                "status": False,
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({
                "status": False,
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)