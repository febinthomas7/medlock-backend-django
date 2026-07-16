from django.db import transaction
from apps.saas_core_admin.models.admins_hospitals import Hospital
from apps.hr_attendance_department.models.departments import Department
from apps.hr_attendance_department.models.hrs import Doctor, Nurse, Receptionist

def _get_staff_model(role):
    role_map = {
        'doctor': Doctor,
        'nurse': Nurse,
        'receptionist': Receptionist
    }
    return role_map.get(str(role).lower())

def create_hospital(admin_user, data):
    with transaction.atomic():
        return Hospital.objects.create(
            admin=admin_user,
            name=data.get('name'),
            email=data.get('email', ''),
            address=data.get('address', ''),
            npi_id=data.get('npi', ''),
            contact_number=data.get('contact', ''),
            image_url=data.get('image', ''),
            state=data.get('state', ''),
            district=data.get('district', ''),
            is_active=True
        )

def update_hospital(admin_user, data):
    hospital_id = data.get('id')
    if not hospital_id:
        raise ValueError("Hospital ID is required for updating.")

    hospital = Hospital.objects.get(id=hospital_id, admin=admin_user)
    
    if 'name' in data: hospital.name = data.get('name')
    if 'email' in data: hospital.email = data.get('email')
    if 'address' in data: hospital.address = data.get('address')
    if 'npi' in data: hospital.npi_id = data.get('npi')
    if 'contact' in data: hospital.contact_number = data.get('contact')
    if 'image' in data: hospital.image_url = data.get('image')
    if 'state' in data: hospital.state = data.get('state')
    if 'district' in data: hospital.district = data.get('district')
    hospital.save()
    
    return hospital

def create_department(user, role, data):
    with transaction.atomic():
        is_active_val = str(data.get('is_active', 'true')).lower() == 'true'

        if role in ['hp', 'hospital']:
            hospital = user  # The user IS the hospital
        elif role in ['ad', 'admin']:
            hospital_id = data.get('hospital_id')
            if not hospital_id or str(hospital_id).lower() == "auto":
                raise ValueError("Valid Hospital ID is required to create a department.")
            hospital = Hospital.objects.get(id=hospital_id, admin=user)
        else:
            raise ValueError("Unauthorized role for department creation.")

        return Department.objects.create(
            hospital=hospital,
            name=data.get('name'),
            password=data.get('password'),
            building_id=data.get('building_id', ''),
            floor=data.get('floor', ''),
            is_active=is_active_val
        )

def update_department(user, role, data):
    department_id = data.get('id')
    if not department_id:
        raise ValueError("Department ID is required for updating.")

    if role in ['hp', 'hospital']:
        department = Department.objects.get(id=department_id, hospital=user)
    elif role in ['ad', 'admin']:
        department = Department.objects.get(id=department_id, hospital__admin=user)
    else:
        raise ValueError("Unauthorized role for department update.")
    
    if 'name' in data: department.name = data.get('name')
    if 'password' in data: department.password = data.get('password')
    if 'building_id' in data: department.building_id = data.get('building_id')
    if 'floor' in data: department.floor = data.get('floor')
    if 'is_active' in data: department.is_active = str(data.get('is_active')).lower() == 'true'
    department.save()
    
    return department

def create_staff(user, auth_role, data):
    """Creates a new staff member with 3-tier RBAC verification"""
    role = data.get('role')
    department_id = data.get('department_id')
    Model = _get_staff_model(role)

    if not Model:
        raise ValueError("Valid role is required.")

    user_type = user.__class__.__name__

    with transaction.atomic():
        # --- 1. 3-TIER SECURITY CHECK FOR TARGET DEPARTMENT ---
        if user_type == 'Department':
            # Department can only add staff directly to itself
            department = user
        else:
            if not department_id:
                raise ValueError("Department ID is required.")
            
            if user_type == 'Hospital':
                # Hospital can add to any of its own departments
                department = Department.objects.get(id=department_id, hospital=user)
            elif user_type == 'Admin':
                # Admin can add to any department in their network
                department = Department.objects.get(id=department_id, hospital__admin=user)
            else:
                raise ValueError("Unauthorized role for staff creation.")

        is_active_val = str(data.get('is_active', 'true')).lower() == 'true'

        # Build staff data securely
        staff_fields = {
            "department": department,
            "name": data.get('name'),
            "password": data.get('password'),
            "adhaar": data.get('adhaar'),
            "contact": data.get('contact'),
            "gmail": data.get('gmail'),
            "address": data.get('address'),
            "punch_id": data.get('punch_id', 0),
            "is_active": is_active_val
        }

        # Add designation if the staff member is a doctor
        if role == 'doctor' and 'designation' in data:
            staff_fields['designation'] = data.get('designation')

        staff_member = Model.objects.create(**staff_fields)
        
    return staff_member, role

def update_staff(user, auth_role, data):
    """Updates an existing staff member with 3-tier RBAC verification"""
    role = data.get('role')
    staff_id = data.get('id')
    Model = _get_staff_model(role)

    if not Model or not staff_id:
        raise ValueError("Valid role and staff ID are required.")

    user_type = user.__class__.__name__

    with transaction.atomic():
        # --- 1. 3-TIER SECURITY CHECK FOR RECORD OWNERSHIP ---
        if user_type == 'Department':
            # Department can only update its own staff
            staff_member = Model.objects.get(id=staff_id, department=user)
        elif user_type == 'Hospital':
            # Hospital can update any staff in its branch
            staff_member = Model.objects.get(id=staff_id, department__hospital=user)
        elif user_type == 'Admin':
            # Admin can update anyone in the network
            staff_member = Model.objects.get(id=staff_id, department__hospital__admin=user)
        else:
            raise ValueError("Unauthorized role for staff update.")

        # --- 2. 3-TIER SECURITY CHECK FOR DEPARTMENT TRANSFERS ---
        new_department_id = data.get('department_id')
        if new_department_id and str(new_department_id) != str(staff_member.department_id):
            if user_type == 'Department':
                raise ValueError("Departments are not authorized to transfer staff to other wings.")
            elif user_type == 'Hospital':
                new_department = Department.objects.get(id=new_department_id, hospital=user)
            elif user_type == 'Admin':
                new_department = Department.objects.get(id=new_department_id, hospital__admin=user)
            
            staff_member.department = new_department

        # --- 3. UPDATE FIELDS DYNAMICALLY ---
        if 'name' in data: staff_member.name = data.get('name')
        if 'password' in data and data.get('password'): staff_member.password = data.get('password')
        if 'adhaar' in data and data.get('adhaar'): staff_member.adhaar = data.get('adhaar')
        if 'contact' in data: staff_member.contact = data.get('contact')
        if 'gmail' in data: staff_member.gmail = data.get('gmail')
        if 'address' in data: staff_member.address = data.get('address')
        if 'punch_id' in data: staff_member.punch_id = data.get('punch_id')
        if 'is_active' in data: staff_member.is_active = str(data.get('is_active')).lower() == 'true'

        # Update designation if the staff member is a doctor
        if role == 'doctor' and 'designation' in data:
            staff_member.designation = data.get('designation')

        staff_member.save()
        
    return staff_member, role