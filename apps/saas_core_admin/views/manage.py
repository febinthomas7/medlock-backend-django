from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db import transaction

# Import your Hospital model
from apps.saas_core_admin.models.admins_hospitals import Hospital
from apps.hr_attendance_department.models.departments import Department
from apps.hr_attendance_department.models.hrs import Doctor, Nurse, Receptionist

class HospitalManagementView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Register a new hospital branch"""
        admin_user = request.user
        data = request.data

        try:
            with transaction.atomic():
                # Map frontend formData fields to your Django model fields.
                # Note: Adjust field names (e.g., npi_id, contact_number) if your model uses different names.
                hospital = Hospital.objects.create(
                    admin=admin_user,
                    name=data.get('name'),
                    email=data.get('email', ''),
                    address=data.get('address', ''),
                    # Using typical pythonic field names, map these to whatever your models.py uses
                    npi_id=data.get('npi', ''), 
                    contact_number=data.get('contact', ''),
                    image_url=data.get('image', ''),
                    state=data.get('state', ''),
                    district=data.get('district', ''),
                    is_active=True 
                )

            # The frontend expects { status: true, id: new_id }
            return Response({
                "status": True,
                "id": str(hospital.id),
                "message": "Hospital registered successfully"
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                "status": False,
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request):
        """Update an existing hospital branch"""
        admin_user = request.user
        data = request.data
        hospital_id = data.get('id')

        if not hospital_id:
            return Response({
                "status": False, 
                "message": "Hospital ID is required for updating."
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Ensure the admin owns this hospital before updating
            hospital = Hospital.objects.get(id=hospital_id, admin=admin_user)
            
            # Update fields dynamically if they are present in the request
            if 'name' in data: hospital.name = data.get('name')
            if 'email' in data: hospital.email = data.get('email')
            if 'address' in data: hospital.address = data.get('address')
            if 'npi' in data: hospital.npi_id = data.get('npi')
            if 'contact' in data: hospital.contact_number = data.get('contact')
            if 'image' in data: hospital.image_url = data.get('image')
            if 'state' in data: hospital.state = data.get('state')
            if 'district' in data: hospital.district = data.get('district')

            hospital.save()

            return Response({
                "status": True,
                "id": str(hospital.id),
                "message": "Hospital updated successfully"
            }, status=status.HTTP_200_OK)

        except Hospital.DoesNotExist:
            return Response({
                "status": False,
                "message": "Hospital not found or you do not have permission to edit it."
            }, status=status.HTTP_404_NOT_FOUND)
            
        except Exception as e:
            return Response({
                "status": False,
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)



class DepartmentManagementView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Fetch all departments belonging to the current admin's hospitals"""
        admin_user = request.user
        
        try:
            # Double underscore (hospital__admin) lets us filter departments 
            # by the admin who owns their parent hospital.
            departments = Department.objects.filter(hospital__admin=admin_user).values(
                'id', 'name', 'password', 'building_id', 'floor', 'is_active', 'hospital_id'
            )
            
            return Response({
                "status": True,
                "departments": list(departments)
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                "status": False,
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        """Register a new department under a specific hospital"""
        admin_user = request.user
        data = request.data
        hospital_id = data.get('hospital_id')

        if not hospital_id:
            return Response({
                "status": False, 
                "message": "Hospital ID is required to create a department."
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                # Security Check: Ensure the admin actually owns this hospital
                hospital = Hospital.objects.get(id=hospital_id, admin=admin_user)
                
                # Parse is_active string from frontend ("true" / "false") to boolean
                is_active_val = str(data.get('is_active', 'true')).lower() == 'true'

                department = Department.objects.create(
                    hospital=hospital,
                    name=data.get('name'),
                    password=data.get('password'),
                    building_id=data.get('building_id', ''),
                    floor=data.get('floor', ''),
                    is_active=is_active_val
                )

            return Response({
                "status": True,
                "id": str(department.id),
                "message": "Department registered successfully"
            }, status=status.HTTP_201_CREATED)

        except Hospital.DoesNotExist:
            return Response({
                "status": False,
                "message": "Hospital not found or you do not have permission to add departments to it."
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({
                "status": False,
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request):
        """Update an existing department"""
        admin_user = request.user
        data = request.data
        department_id = data.get('id')

        if not department_id:
            return Response({
                "status": False, 
                "message": "Department ID is required for updating."
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Security Check: Fetch the department ONLY if the admin owns the parent hospital
            department = Department.objects.get(id=department_id, hospital__admin=admin_user)
            
            # Update fields dynamically
            if 'name' in data: 
                department.name = data.get('name')
            if 'password' in data: 
                department.password = data.get('password')
            if 'building_id' in data: 
                department.building_id = data.get('building_id')
            if 'floor' in data: 
                department.floor = data.get('floor')
            if 'is_active' in data: 
                department.is_active = str(data.get('is_active')).lower() == 'true'

            department.save()

            return Response({
                "status": True,
                "id": str(department.id),
                "message": "Department updated successfully"
            }, status=status.HTTP_200_OK)

        except Department.DoesNotExist:
            return Response({
                "status": False,
                "message": "Department not found or you do not have permission to edit it."
            }, status=status.HTTP_404_NOT_FOUND)
            
        except Exception as e:
            return Response({
                "status": False,
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)



class StaffManagementView(APIView):
    permission_classes = [IsAuthenticated]

    def _get_model(self, role):
        """Helper method to determine which model to use"""
        role_map = {
            'doctor': Doctor,
            'nurse': Nurse,
            'receptionist': Receptionist
        }
        return role_map.get(str(role).lower())

    def get(self, request):
        """Fetch staff members by role for the current admin's network"""
        role = request.query_params.get('role')
        Model = self._get_model(role)
        
        if not Model:
            return Response({
                "status": False, 
                "message": "Invalid or missing role parameter. Use 'doctor', 'nurse', or 'receptionist'."
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Filter staff belonging to a department whose parent hospital is owned by this admin
            staff_queryset = Model.objects.filter(department__hospital__admin=request.user).select_related('department', 'department__hospital')
            
            staff_data = []
            for staff in staff_queryset:
                staff_data.append({
                    "id": str(staff.id),
                    "name": staff.name,
                    "gmail": staff.gmail,
                    "contact": staff.contact,
                    "address": staff.address,
                    "punch_id": staff.punch_id,
                    "is_active": staff.is_active,
                    "department_id": staff.department.id if staff.department else None,
                    "department__name": staff.department.name if staff.department else "N/A",
                    "hospital_id": staff.department.hospital.id if staff.department else None,
                    # DO NOT OUTPUT RAW AADHAAR TO FRONTEND - Privacy compliance
                    "adhaar": "[Aadhaar Redacted]", 
                    # Only include designation if the model actually has it (e.g., Doctor)
                    "designation": getattr(staff, 'designation', None)
                })

            return Response({
                "status": True,
                "staff": staff_data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({"status": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        """Register a new staff member to a department"""
        admin_user = request.user
        data = request.data
        
        role = data.get('role')
        Model = self._get_model(role)
        department_id = data.get('department_id')

        if not Model or not department_id:
            return Response({
                "status": False, 
                "message": "Valid role and department_id are required."
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                # Security Check: Ensure the admin owns the hospital this department belongs to
                department = Department.objects.get(id=department_id, hospital__admin=admin_user)
                
                is_active_val = str(data.get('is_active', 'true')).lower() == 'true'

                # Build the base dictionary for all staff types
                staff_fields = {
                    "department": department,
                    "name": data.get('name'),
                    "password": data.get('password'),
                    "adhaar": data.get('adhaar'),
                    "contact": data.get('contact'),
                    "gmail": data.get('gmail'),
                    "address": data.get('address'),
                    "punch_id": data.get('punch_id', 0), # Fallback to 0 if not provided
                    "is_active": is_active_val
                }

                # Add specific fields for Doctors only
                if role == 'doctor' and 'designation' in data:
                    staff_fields['designation'] = data.get('designation')

                # Create the staff member
                staff_member = Model.objects.create(**staff_fields)

            return Response({
                "status": True,
                "id": str(staff_member.id),
                "message": f"{role.capitalize()} registered successfully"
            }, status=status.HTTP_201_CREATED)

        except Department.DoesNotExist:
            return Response({
                "status": False,
                "message": "Department not found or you do not have permission to add staff to it."
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"status": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        """Update an existing staff member"""
        admin_user = request.user
        data = request.data
        
        role = data.get('role')
        Model = self._get_model(role)
        staff_id = data.get('id')

        if not Model or not staff_id:
            return Response({
                "status": False, 
                "message": "Valid role and staff ID are required."
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Security Check: Fetch the staff member ONLY if the admin owns their parent hospital
            staff_member = Model.objects.get(id=staff_id, department__hospital__admin=admin_user)
            
            # Handle changing departments (must verify new department ownership)
            new_department_id = data.get('department_id')
            if new_department_id and str(new_department_id) != str(staff_member.department_id):
                new_department = Department.objects.get(id=new_department_id, hospital__admin=admin_user)
                staff_member.department = new_department

            # Update fields dynamically
            if 'name' in data: staff_member.name = data.get('name')
            if 'password' in data: staff_member.password = data.get('password')
            if 'adhaar' in data and data.get('adhaar'): staff_member.adhaar = data.get('adhaar')
            if 'contact' in data: staff_member.contact = data.get('contact')
            if 'gmail' in data: staff_member.gmail = data.get('gmail')
            if 'address' in data: staff_member.address = data.get('address')
            if 'punch_id' in data: staff_member.punch_id = data.get('punch_id')
            if 'is_active' in data: staff_member.is_active = str(data.get('is_active')).lower() == 'true'

            # Doctor only fields
            if role == 'doctor' and 'designation' in data:
                staff_member.designation = data.get('designation')

            staff_member.save()

            return Response({
                "status": True,
                "id": str(staff_member.id),
                "message": f"{role.capitalize()} updated successfully"
            }, status=status.HTTP_200_OK)

        except Model.DoesNotExist:
            return Response({
                "status": False,
                "message": "Staff member not found or you do not have permission to edit them."
            }, status=status.HTTP_404_NOT_FOUND)
            
        except Department.DoesNotExist:
            return Response({
                "status": False,
                "message": "Target department not found or unauthorized."
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({"status": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
