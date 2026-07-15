from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db.models import Count, OuterRef, Subquery, IntegerField
from django.db.models.functions import Coalesce

# Import your models based on your structure
from apps.saas_core_admin.models.admins_hospitals import Admin, Hospital
from apps.hr_attendance_department.models.hrs import Doctor, Receptionist
from apps.user.models.medical import UserReport

class AdminBranchListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user 
            
            # --- BULLETPROOF ROLE CHECK ---
            if user.__class__.__name__ == 'Hospital':
                # Hospital only sees its own data
                admin_hospitals = Hospital.objects.filter(id=user.id)
            else:
                # Admin sees all hospitals under their account
                admin_hospitals = Hospital.objects.filter(admin=user)

            # 2. Define Subqueries for Per-Hospital Counts 
            docs_sq = Doctor.objects.filter(
                department__hospital_id=OuterRef('pk')
            ).values('department__hospital_id').annotate(count=Count('id')).values('count')

            receps_sq = Receptionist.objects.filter(
                department__hospital_id=OuterRef('pk')
            ).values('department__hospital_id').annotate(count=Count('id')).values('count')

            reports_sq = UserReport.objects.filter(
                hospital_id=OuterRef('pk')
            ).values('hospital_id').annotate(count=Count('id')).values('count')

            # 3. Annotate the hospitals with the counts
            hospitals_with_stats = admin_hospitals.annotate(
                doctors_count=Coalesce(Subquery(docs_sq, output_field=IntegerField()), 0),
                receptionists_count=Coalesce(Subquery(receps_sq, output_field=IntegerField()), 0),
                reports_count=Coalesce(Subquery(reports_sq, output_field=IntegerField()), 0)
            )

            hospitals_data = []

            # 4. Serialize data
            for hospital in hospitals_with_stats:
                # Safely get state/district whether they are fields, foreign keys, or missing entirely
                raw_state = getattr(hospital, 'state', 'N/A')
                raw_district = getattr(hospital, 'district', 'N/A')
                
                state_name = raw_state.name if hasattr(raw_state, 'name') else str(raw_state)
                district_name = raw_district.name if hasattr(raw_district, 'name') else str(raw_district)
                
                hospitals_data.append({
                    "id": str(hospital.id),
                    "Name": hospital.name,
                    "Status__c": getattr(hospital, 'status', 'Active'),
                    "State__r": {
                        "Name": state_name
                    },
                    "District__r": {
                        "Name": district_name
                    },
                    "counts": {
                        "reports": hospital.reports_count,
                        "doctors": hospital.doctors_count,
                        "receptionists": hospital.receptionists_count,
                    }
                })

            return Response({
                "status": True,
                "hospitals": hospitals_data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "status": False,
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)