from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist

from apps.saas_core_admin.models.admins_hospitals import Hospital
from apps.hr_attendance_department.models.departments import Department

# Import your newly extracted layers
from apps.saas_core_admin.services import manage as services
from apps.saas_core_admin.selectors import manage as selectors
from apps.plugin_rbac.permissions.navigation import HasRBACPermission


class HospitalManagementView(APIView):
    permission_classes = [IsAuthenticated, HasRBACPermission]
    required_rbac_permission = "Hospital Management"

    def post(self, request):
        try:
            hospital = services.create_hospital(request.user, request.data)
            return Response({
                "status": True,
                "id": str(hospital.id),
                "message": "Hospital registered successfully"
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"status": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        try:
            hospital = services.update_hospital(request.user, request.data)
            return Response({
                "status": True,
                "id": str(hospital.id),
                "message": "Hospital updated successfully"
            }, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"status": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Hospital.DoesNotExist:
            return Response({
                "status": False,
                "message": "Hospital not found or you do not have permission to edit it."
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class DepartmentManagementView(APIView):
    permission_classes = [IsAuthenticated, HasRBACPermission]
    required_rbac_permission = "Department Management"

    def get(self, request):
        try:
            user = request.user
            user_type = user.__class__.__name__
            
            # --- 3-TIER BULLETPROOF ROLE ROUTING ---
            if user_type == 'Hospital':
                departments = selectors.get_departments_by_hospital(user)
            elif user_type == 'Admin':
                departments = selectors.get_departments_for_admin(user)
            elif user_type == 'Department':
                # Department only needs to see itself to populate the dropdown
                departments = selectors.get_department_for_self(user)
            else:
                return Response({"status": False, "message": "Unauthorized role"}, status=status.HTTP_403_FORBIDDEN)
            
            return Response({
                "status": True,
                "departments": departments
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({"status": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            role = request.auth.get('role', '').lower()
            department = services.create_department(request.user, role, request.data)
            
            return Response({
                "status": True,
                "id": str(department.id),
                "message": "Department registered successfully"
            }, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"status": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Hospital.DoesNotExist:
            return Response({
                "status": False,
                "message": "Hospital not found or unauthorized."
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        try:
            role = request.auth.get('role', '').lower()
            department = services.update_department(request.user, role, request.data)
            
            return Response({
                "status": True,
                "id": str(department.id),
                "message": "Department updated successfully"
            }, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"status": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Department.DoesNotExist:
            return Response({
                "status": False,
                "message": "Department not found or unauthorized."
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)



class StaffManagementView(APIView):
    permission_classes = [IsAuthenticated, HasRBACPermission]
    required_rbac_permission = "Staff Management"

    def get(self, request):
        try:
            role = request.query_params.get('role')
            if not role:
                return Response({"status": False, "message": "Staff role query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

            user = request.user
            user_type = user.__class__.__name__
            
            # --- 3-TIER BULLETPROOF ROLE ROUTING ---
            if user_type == 'Hospital':
                staff_data = selectors.get_staff_for_hospital(user, role)
            elif user_type == 'Department':
                staff_data = selectors.get_staff_for_department(user, role)
            elif user_type == 'Admin':
                staff_data = selectors.get_staff_for_admin(user, role)
            else:
                return Response({"status": False, "message": "Unauthorized role"}, status=status.HTTP_403_FORBIDDEN)

            return Response({
                "status": True,
                "staff": staff_data
            }, status=status.HTTP_200_OK)
            
        except ValueError as e:
            return Response({"status": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"status": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            # Extract auth_role from JWT to pass down to the service layer
            auth_role = request.auth.get('role', '').lower()
            
            # Assuming your service layer is updated to accept the auth_role
            staff_member, role = services.create_staff(request.user, auth_role, request.data)
            
            return Response({
                "status": True,
                "id": str(staff_member.id),
                "message": f"{role.capitalize()} registered successfully"
            }, status=status.HTTP_201_CREATED)
            
        except ValueError as e:
            return Response({"status": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Department.DoesNotExist:
            return Response({
                "status": False,
                "message": "Department not found or unauthorized."
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        try:
            auth_role = request.auth.get('role', '').lower()
            staff_member, role = services.update_staff(request.user, auth_role, request.data)
            
            return Response({
                "status": True,
                "id": str(staff_member.id),
                "message": f"{role.capitalize()} updated successfully"
            }, status=status.HTTP_200_OK)
            
        except ValueError as e:
            return Response({"status": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Department.DoesNotExist:
            return Response({"status": False, "message": "Target department not found or unauthorized."}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({"status": False, "message": "Staff member not found or unauthorized."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)