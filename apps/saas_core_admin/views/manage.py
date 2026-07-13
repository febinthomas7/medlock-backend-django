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


class HospitalManagementView(APIView):
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            departments = selectors.get_departments_for_admin(request.user)
            return Response({
                "status": True,
                "departments": departments
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            department = services.create_department(request.user, request.data)
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
            department = services.update_department(request.user, request.data)
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
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            role = request.query_params.get('role')
            staff_data = selectors.get_staff_for_admin(request.user, role)
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
            staff_member, role = services.create_staff(request.user, request.data)
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
            staff_member, role = services.update_staff(request.user, request.data)
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