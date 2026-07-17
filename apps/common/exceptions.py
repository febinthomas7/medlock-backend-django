
from django.core.exceptions import ValidationError

class InvalidDepartmentWardError(ValidationError):
    """
    Raised when an attempt is made to attach an inpatient ward 
    to a specialized, non-clinical plugin wing.
    """
    def __init__(self, department_name, required_type):
        message = (
            f"Inpatient Wards cannot be created inside a {department_name}. "
            f"Wards are restricted to {required_type} wings only."
        )
        super().__init__(message)

class InvalidStaffRoleError(ValidationError):
    """
    Raised when a staff assignment violates the isolated plugin rulebook.
    """
    def __init__(self, role, department_name):
        message = (
            f"A standard {role} cannot be assigned to the {department_name}. "
            f"Please use the specialized staff portal for this department."
        )
        super().__init__(message)