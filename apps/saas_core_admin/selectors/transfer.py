from apps.hr_attendance_department.models.hrs import Doctor, Nurse, Receptionist

def get_staff_model(role):
    """Helper method to determine which model to use based on the string role."""
    role_map = {
        'doctor': Doctor,
        'nurse': Nurse,
        'receptionist': Receptionist
    }
    return role_map.get(str(role).lower())