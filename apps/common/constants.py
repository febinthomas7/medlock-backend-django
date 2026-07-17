

STANDARD_DEPARTMENT_TYPE = 'DP'

PLUGIN_DEPARTMENT_CONFIG = {
    'IS': {
        'name_suffix': 'Insurance Wing',
        'roles': {
            'Doctor': 'ID',       # Insurance Doctor
            'Nurse': 'IN',        # Insurance Nurse / Case Manager
            'Receptionist': 'IR'  # Insurance Receptionist
        }
    },
    'BB': {
        'name_suffix': 'Blood Bank',
        'roles': {
            'Doctor': 'BD',       # Blood Bank Doctor / Pathologist
            'Nurse': 'BN',        # Blood Bank Nurse / Phlebotomist
            'Receptionist': 'BR'  # Blood Bank Receptionist
        }
    },
    'PT': {
        'name_suffix': 'Pathology Lab',
        'roles': {
            'Doctor': 'PD',       # Pathologist
            'Nurse': 'PL',        # Lab Technician
            'Receptionist': 'PR'  # Lab Receptionist
        }
    },
    'RD': {
        'name_suffix': 'Radiology Center',
        'roles': {
            'Doctor': 'RD',       # Radiologist
            'Nurse': 'RT',        # Imaging Technician
            'Receptionist': 'RR'  # Radiology Receptionist
        }
    },
    'DE': {
        'name_suffix': 'Dental Clinic',
        'roles': {
            'Doctor': 'DD',       # Dental Doctor / Dentist
            'Nurse': 'DA',        # Dental Assistant / Hygienist
            'Receptionist': 'DC'  # Dental Clerk
        }
    }
}


# Storing as "app_label.ModelName" prevents circular import crashes during Django boot for login
ROLE_MODEL_MAP = {
    # Admin & Hospital
    "admin": "saas_core_admin.Admin", 
    "ad": "saas_core_admin.Admin",
    "hospital": "saas_core_admin.Hospital", 
    "hp": "saas_core_admin.Hospital",
    
    # Departments
    "department": "hr_attendance_department.Department", 
    "dp": "hr_attendance_department.Department",
    "insurance": "hr_attendance_department.Department", 
    "is": "hr_attendance_department.Department",
    
    # Wards & Rooms
    "ward": "hr_attendance_department.Ward", 
    "wr": "hr_attendance_department.Ward",
    "room": "hr_attendance_department.Room", 
    "rm": "hr_attendance_department.Room",
    
    # Clinical Staff
    "doctor": "hr_attendance_department.Doctor", 
    "dr": "hr_attendance_department.Doctor",
    "nurse": "hr_attendance_department.Nurse", 
    "ns": "hr_attendance_department.Nurse",
    "receptionist": "hr_attendance_department.Receptionist", 
    "rs": "hr_attendance_department.Receptionist",
    
    # Insurance Staff (Mapped to standard models, but isolated by prefix)
    "id": "hr_attendance_department.Doctor",
    "in": "hr_attendance_department.Nurse",
    "ir": "hr_attendance_department.Receptionist"
}


# Role expansions for navigation and RBAC checks 
ROLE_EXPANSIONS = {
    'admin': ['admin', 'ad'],
    'ad': ['admin', 'ad'],
    'hospital': ['hospital', 'hp'],
    'hp': ['hospital', 'hp'],
    
    # Standard Clinical Roles
    'department': ['department', 'dp'],
    'dp': ['department', 'dp'],
    'doctor': ['doctor', 'dr'],
    'dr': ['doctor', 'dr'],
    'nurse': ['nurse', 'ns'],
    'ns': ['nurse', 'ns'],
    'receptionist': ['receptionist', 'rs'],
    'rs': ['receptionist', 'rs'],
    
    # --- NEW: Insurance Plugin Roles ---
    'insurance': ['insurance', 'is'],
    'is': ['insurance', 'is'],
    'id': ['id', 'insurance_doctor'],
    'in': ['in', 'insurance_nurse'],
    'ir': ['ir', 'insurance_receptionist'],
}