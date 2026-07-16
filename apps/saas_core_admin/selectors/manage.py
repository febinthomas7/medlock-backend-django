from apps.hr_attendance_department.models.departments import Department
from apps.hr_attendance_department.models.hrs import Doctor, Nurse, Receptionist

def _get_staff_model(role):
    """Helper method to determine which model to use"""
    role_map = {
        'doctor': Doctor,
        'nurse': Nurse,
        'receptionist': Receptionist
    }
    return role_map.get(str(role).lower())

# --- ADMIN SELECTOR ---
def get_departments_for_admin(admin_user):
    """Fetches all departments belonging to the given admin."""
    departments = Department.objects.filter(hospital__admin=admin_user).values(
        'id', 'name', 'password', 'building_id', 'floor', 'is_active', 'hospital_id'
    )
    return list(departments)

# --- HOSPITAL SELECTOR (NEW) ---
def get_departments_by_hospital(hospital_user):
    """Fetches departments only for the specific logged-in hospital."""
    departments = Department.objects.filter(hospital=hospital_user).values(
        'id', 'name', 'password', 'building_id', 'floor', 'is_active', 'hospital_id'
    )
    return list(departments)

# --- DEPARTMENT SELECTOR (NEW) ---
def get_department_for_self(department_user):
    """Fetches only the specific logged-in department."""
    departments = Department.objects.filter(id=department_user.id).values(
        'id', 'name', 'password', 'building_id', 'floor', 'is_active', 'hospital_id'
    )
    return list(departments)

def get_staff_for_admin(admin_user, role):
    Model = _get_staff_model(role)
    if not Model:
        raise ValueError("Invalid or missing role parameter.")

    staff_queryset = Model.objects.filter(
        department__hospital__admin=admin_user
    ).select_related('department', 'department__hospital')
    
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
            "adhaar": "[Aadhaar Redacted]", 
            "designation": getattr(staff, 'designation', None)
        })
        
    return staff_data

def get_staff_for_hospital(hospital_user, role):
    """Fetches staff members by role for the given hospital."""
    Model = _get_staff_model(role)
    if not Model:
        raise ValueError("Invalid or missing role parameter.")

    # Filter strictly by the hospital user
    staff_queryset = Model.objects.filter(
        department__hospital=hospital_user
    ).select_related('department', 'department__hospital')
    
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
            "adhaar": "[Aadhaar Redacted]", 
            "designation": getattr(staff, 'designation', None)
        })
        
    return staff_data


def get_staff_for_department(department_user, role):
    """Fetches staff members by role for the specific department."""
    Model = _get_staff_model(role)
    if not Model:
        raise ValueError("Invalid or missing role parameter.")

    # Filter strictly by the department user
    staff_queryset = Model.objects.filter(
        department=department_user
    ).select_related('department', 'department__hospital')
    
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
            "adhaar": "[Aadhaar Redacted]", 
            "designation": getattr(staff, 'designation', None)
        })
        
    return staff_data