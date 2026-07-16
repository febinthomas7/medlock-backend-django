from django.db import transaction
from apps.hr_attendance_department.models.departments import Department
from apps.saas_core_admin.selectors import transfer as selectors

def execute_staff_transfer(user, role, staff_id, new_department_id):
    """Executes the staff transfer with strict 3-tier RBAC enforcement."""
    
    Model = selectors.get_staff_model(role)
    if not Model:
        raise ValueError(f"Invalid staff role specified: {role}")

    user_type = user.__class__.__name__

    with transaction.atomic():
        # --- 1. BLOCK DEPARTMENT LEVEL TRANSFERS ---
        if user_type == 'Department':
            raise PermissionError("Department-level users are not authorized to perform staff transfers.")

        # --- 2. VERIFY DESTINATION OWNERSHIP ---
        if user_type == 'Hospital':
            # Hospital can only transfer into its own departments
            new_department = Department.objects.get(id=new_department_id, hospital=user)
        elif user_type == 'Admin':
            # Admin can transfer into any department in their network
            new_department = Department.objects.get(id=new_department_id, hospital__admin=user)
        else:
            raise PermissionError("Unauthorized role for staff transfer.")

        # --- 3. VERIFY STAFF MEMBER OWNERSHIP ---
        if user_type == 'Hospital':
            # Hospital can only pull staff that already exist in their branch
            staff_member = Model.objects.get(id=staff_id, department__hospital=user)
        elif user_type == 'Admin':
            # Admin can pull any staff member in their network
            staff_member = Model.objects.get(id=staff_id, department__hospital__admin=user)

        # --- 4. PREVENT REDUNDANT TRANSFERS ---
        if str(staff_member.department_id) == str(new_department_id):
            raise ValueError("Staff member is already assigned to this department.")

        # --- 5. EXECUTE TRANSFER ---
        staff_member.department = new_department
        staff_member.save()

    return staff_member, new_department