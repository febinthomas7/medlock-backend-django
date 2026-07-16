from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db.models import Count, Q
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth
from django.utils import timezone
from datetime import timedelta

# Import your models
from apps.saas_core_admin.models.admins_hospitals import Admin, Hospital
from apps.hr_attendance_department.models.departments import Department, Ward, Room
from apps.hr_attendance_department.models.hrs import Doctor, Nurse, Receptionist
from apps.user.models.medical import UserAppointment, UserReport

class UnifiedDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            user_type = user.__class__.__name__

            # 1. Capture query parameters sent by the Unified Filter Bar
            hospital_id = request.query_params.get('hospital_id', 'all')
            department_id = request.query_params.get('department_id', 'all')
            timeframe = request.query_params.get('timeframe', 'week')
            from_date = request.query_params.get('from_date')
            to_date = request.query_params.get('to_date')

            date_filters = Q()
            if from_date and to_date:
                date_filters &= Q(created_at__range=[from_date, to_date])

            # --- 2. 3-TIER RBAC SCOPING ENGINE ---
            target_hospital_ids = []
            target_department_ids = []

            if user_type == 'Admin':
                # Admin can filter across network
                h_qs = Hospital.objects.filter(admin=user)
                if hospital_id != 'all':
                    h_qs = h_qs.filter(id=hospital_id)
                target_hospital_ids = list(h_qs.values_list('id', flat=True))

                d_qs = Department.objects.filter(hospital_id__in=target_hospital_ids)
                if department_id != 'all':
                    d_qs = d_qs.filter(id=department_id)
                target_department_ids = list(d_qs.values_list('id', flat=True))

            elif user_type == 'Hospital':
                # Hospital is locked to itself
                target_hospital_ids = [user.id]
                d_qs = Department.objects.filter(hospital=user)
                if department_id != 'all':
                    d_qs = d_qs.filter(id=department_id)
                target_department_ids = list(d_qs.values_list('id', flat=True))

            elif user_type == 'Department':
                # Department is strictly locked to its own ID
                target_hospital_ids = [user.hospital_id]
                target_department_ids = [user.id]

            else:
                return Response({"status": False, "message": "Unauthorized access"}, status=status.HTTP_403_FORBIDDEN)

            # --- 3. CALCULATE CORE STATS ---
            # Staff is aggregated securely based on the allowed department IDs
            total_docs = Doctor.objects.filter(department_id__in=target_department_ids).count()
            total_nurses = Nurse.objects.filter(department_id__in=target_department_ids).count()
            total_receps = Receptionist.objects.filter(department_id__in=target_department_ids).count()
            
            # Reports & Appts are aggregated by allowed hospital IDs
            # (If your models have department relationships, change to department_id__in=target_department_ids)
            total_appts = UserAppointment.objects.filter(hospital_id__in=target_hospital_ids).filter(date_filters).count()
            total_reports = UserReport.objects.filter(hospital_id__in=target_hospital_ids).filter(date_filters).count()

            stats_data = {
                "totalReports": total_reports,
                "totalAppointments": total_appts,
                "totalDocs": total_docs,
                "totalNurses": total_nurses,
                "totalReceps": total_receps,
                "avgGrowth": "+12.4%" # Could be dynamically calculated based on previous timeframe
            }

            # --- 4. GENERATE TIME-SERIES CHART DATA ---
            chart_data = self.get_chart_data(target_hospital_ids, timeframe)

            # --- 5. DATA FOR SECONDARY CHARTS ---
            # NOTE: These are fallback payloads to render the new Pie/Bar/Radar charts. 
            # You can hook these up to actual Django annotations as your DB grows.
            specialty_data = [
                {"name": "Cardiology", "value": 450},
                {"name": "Neurology", "value": 320},
                {"name": "Pediatrics", "value": 300},
                {"name": "Orthopedics", "value": 280}
            ]

            activity_data = [
                {"name": "Wk 1", "reports": 120},
                {"name": "Wk 2", "reports": 150},
                {"name": "Wk 3", "reports": 180},
                {"name": "Wk 4", "reports": 140}
            ]

            radar_data = [
                {"subject": "Speed", "A": 120, "fullMark": 150},
                {"subject": "Accuracy", "A": 98, "fullMark": 150},
                {"subject": "Volume", "A": 86, "fullMark": 150},
                {"subject": "Feedback", "A": 99, "fullMark": 150}
            ]

            return Response({
                "status": True,
                "stats": stats_data,
                "chart_data": chart_data,
                "specialty_data": specialty_data,
                "activity_data": activity_data,
                "radar_data": radar_data,
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "status": False,
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    def get_chart_data(self, hospital_ids, timeframe):
        """Generates dynamic time-series data for the AreaChart"""
        now = timezone.now()
        chart_dict = {}

        if timeframe == 'week':
            start_date = now - timedelta(days=7)
            
            appts = UserAppointment.objects.filter(hospital_id__in=hospital_ids, created_at__gte=start_date) \
                .annotate(date=TruncDay('created_at')) \
                .values('date').annotate(count=Count('id'))
                
            reports = UserReport.objects.filter(hospital_id__in=hospital_ids, created_at__gte=start_date) \
                .annotate(date=TruncDay('created_at')) \
                .values('date').annotate(count=Count('id'))

            for i in range(7):
                day = start_date + timedelta(days=i)
                chart_dict[day.date()] = {"name": day.strftime('%a'), "appointments": 0, "reports": 0}

            for a in appts:
                if a['date']: chart_dict[a['date'].date()]['appointments'] = a['count']
            for r in reports:
                if r['date']: chart_dict[r['date'].date()]['reports'] = r['count']

            return list(chart_dict.values())

        elif timeframe == 'year':
            start_date = now.replace(month=1, day=1, hour=0, minute=0, second=0)

            appts = UserAppointment.objects.filter(hospital_id__in=hospital_ids, created_at__gte=start_date) \
                .annotate(month=TruncMonth('created_at')) \
                .values('month').annotate(count=Count('id'))

            reports = UserReport.objects.filter(hospital_id__in=hospital_ids, created_at__gte=start_date) \
                .annotate(month=TruncMonth('created_at')) \
                .values('month').annotate(count=Count('id'))

            for month in range(1, 13):
                month_date = start_date.replace(month=month)
                chart_dict[month] = {"name": month_date.strftime('%b'), "appointments": 0, "reports": 0}

            for a in appts:
                if a['month']: chart_dict[a['month'].month]['appointments'] = a['count']
            for r in reports:
                if r['month']: chart_dict[r['month'].month]['reports'] = r['count']

            return list(chart_dict.values())
        
        elif timeframe == 'month':
            start_date = now - timedelta(days=30)
            # Similar TruncDay implementation for month...
            return []

        return []