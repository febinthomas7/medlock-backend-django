from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db import transaction

# Import your models
from apps.hr_attendance_department.models.hrs import Doctor, Nurse, Receptionist
from apps.hr_attendance_department.models.departments import Department

class StaffTransferView(APIView):
    permission_classes = [IsAuthenticated]

    def _get_model(self, role):
        role_map = {
            'doctor': Doctor,
            'nurse': Nurse,
            'receptionist': Receptionist
        }
        return role_map.get(str(role).lower())

    def post(self, request):
        """Transfer a staff member to a new department/hospital"""
        admin_user = request.user
        data = request.data
        
        role = data.get('role')
        staff_id = data.get('staff_id')
        new_department_id = data.get('new_department_id')

        Model = self._get_model(role)

        if not Model or not staff_id or not new_department_id:
            return Response({
                "status": False, 
                "message": "Role, Staff ID, and New Department ID are required."
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                # 1. Verify the admin owns the NEW destination department
                new_department = Department.objects.get(id=new_department_id, hospital__admin=admin_user)
                
                # 2. Fetch the staff member and verify the admin owns their CURRENT location
                staff_member = Model.objects.get(id=staff_id, department__hospital__admin=admin_user)
                
                # 3. Execute the transfer
                staff_member.department = new_department
                staff_member.save()

            return Response({
                "status": True,
                "message": f"{role.capitalize()} successfully transferred to {new_department.name}."
            }, status=status.HTTP_200_OK)

        except Department.DoesNotExist:
            return Response({
                "status": False,
                "message": "Destination department not found or you lack permission to access it."
            }, status=status.HTTP_404_NOT_FOUND)
            
        except Model.DoesNotExist:
            return Response({
                "status": False,
                "message": "Staff member not found or you lack permission to modify them."
            }, status=status.HTTP_404_NOT_FOUND)
            
        except Exception as e:
            return Response({
                "status": False,
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)