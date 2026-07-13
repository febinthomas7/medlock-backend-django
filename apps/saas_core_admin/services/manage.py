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

def create_department(admin_user, data):
    hospital_id = data.get('hospital_id')
    if not hospital_id:
        raise ValueError("Hospital ID is required to create a department.")

    with transaction.atomic():
        hospital = Hospital.objects.get(id=hospital_id, admin=admin_user)
        is_active_val = str(data.get('is_active', 'true')).lower() == 'true'

        return Department.objects.create(
            hospital=hospital,
            name=data.get('name'),
            password=data.get('password'),
            building_id=data.get('building_id', ''),
            floor=data.get('floor', ''),
            is_active=is_active_val
        )

def update_department(admin_user, data):
    department_id = data.get('id')
    if not department_id:
        raise ValueError("Department ID is required for updating.")

    department = Department.objects.get(id=department_id, hospital__admin=admin_user)
    
    if 'name' in data: department.name = data.get('name')
    if 'password' in data: department.password = data.get('password')
    if 'building_id' in data: department.building_id = data.get('building_id')
    if 'floor' in data: department.floor = data.get('floor')
    if 'is_active' in data: department.is_active = str(data.get('is_active')).lower() == 'true'
    department.save()
    
    return department

def create_staff(admin_user, data):
    role = data.get('role')
    department_id = data.get('department_id')
    Model = _get_staff_model(role)

    if not Model or not department_id:
        raise ValueError("Valid role and department_id are required.")

    with transaction.atomic():
        department = Department.objects.get(id=department_id, hospital__admin=admin_user)
        is_active_val = str(data.get('is_active', 'true')).lower() == 'true'

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

        if role == 'doctor' and 'designation' in data:
            staff_fields['designation'] = data.get('designation')

        staff_member = Model.objects.create(**staff_fields)
        
    return staff_member, role

def update_staff(admin_user, data):
    role = data.get('role')
    staff_id = data.get('id')
    Model = _get_staff_model(role)

    if not Model or not staff_id:
        raise ValueError("Valid role and staff ID are required.")

    staff_member = Model.objects.get(id=staff_id, department__hospital__admin=admin_user)
    
    new_department_id = data.get('department_id')
    if new_department_id and str(new_department_id) != str(staff_member.department_id):
        new_department = Department.objects.get(id=new_department_id, hospital__admin=admin_user)
        staff_member.department = new_department

    if 'name' in data: staff_member.name = data.get('name')
    if 'password' in data: staff_member.password = data.get('password')
    if 'adhaar' in data and data.get('adhaar'): staff_member.adhaar = data.get('adhaar')
    if 'contact' in data: staff_member.contact = data.get('contact')
    if 'gmail' in data: staff_member.gmail = data.get('gmail')
    if 'address' in data: staff_member.address = data.get('address')
    if 'punch_id' in data: staff_member.punch_id = data.get('punch_id')
    if 'is_active' in data: staff_member.is_active = str(data.get('is_active')).lower() == 'true'

    if role == 'doctor' and 'designation' in data:
        staff_member.designation = data.get('designation')

    staff_member.save()
    
    return staff_member, role