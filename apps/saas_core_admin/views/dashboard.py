from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Q
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth
from django.utils import timezone
from datetime import timedelta

# Import your models
from apps.saas_core_admin.models.admins_hospitals import Admin, Hospital
from apps.hr_attendance_department.models.departments import Department, Ward, Room
from apps.hr_attendance_department.models.hrs import Doctor, Nurse, Receptionist
from apps.user.models.medical import UserAppointment, UserReport

class AdminDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        admin_user = request.user 
        
        branch_id = request.query_params.get('branch', 'all')
        timeframe = request.query_params.get('timeframe', 'week')
        from_date = request.query_params.get('from_date')
        to_date = request.query_params.get('to_date')

        date_filters = Q()
        if from_date and to_date:
            date_filters &= Q(created_at__range=[from_date, to_date])

        # 1. Fetch Hospitals and Flatten IDs
        admin_hospitals = Hospital.objects.filter(admin=admin_user)
        if branch_id != 'all':
            admin_hospitals = admin_hospitals.filter(id=branch_id)

        hospital_ids = list(admin_hospitals.values_list('id', flat=True))
        hospitals_data = [{"id": str(h.id), "name": h.name} for h in admin_hospitals]

        # 2. CALCULATE STATS 
        # Doctors and Receps still traverse through Department
        total_docs = Doctor.objects.filter(department__hospital_id__in=hospital_ids).count()
        total_receps = Receptionist.objects.filter(department__hospital_id__in=hospital_ids).count()
        
        # 🚀 APPOINTMENTS & REPORTS: Query hospital_id directly!
        total_appts = UserAppointment.objects.filter(hospital_id__in=hospital_ids).filter(date_filters).count()
        total_reports = UserReport.objects.filter(hospital_id__in=hospital_ids).filter(date_filters).count()

        stats_data = {
            "totalReports": total_reports,
            "totalAppointments": total_appts,
            "totalDocs": total_docs,
            "totalReceps": total_receps,
            "avgGrowth": "+0.0%" 
        }

        # 3. GENERATE CHART DATA
        chart_data = self.get_chart_data(hospital_ids, timeframe)

        return Response({
            "hospitals": hospitals_data,
            "stats": stats_data,
            "chart_data": chart_data,
        })

    def get_chart_data(self, hospital_ids, timeframe):
        now = timezone.now()
        chart_dict = {}

        if timeframe == 'week':
            start_date = now - timedelta(days=7)
            
            # 🚀 Use direct hospital_id__in
            appts = UserAppointment.objects.filter(hospital_id__in=hospital_ids, created_at__gte=start_date) \
                .annotate(date=TruncDay('created_at')) \
                .values('date') \
                .annotate(count=Count('id'))
                
            reports = UserReport.objects.filter(hospital_id__in=hospital_ids, created_at__gte=start_date) \
                .annotate(date=TruncDay('created_at')) \
                .values('date') \
                .annotate(count=Count('id'))

            for i in range(7):
                day = start_date + timedelta(days=i)
                day_str = day.strftime('%a')
                chart_dict[day.date()] = {"name": day_str, "appointments": 0, "reports": 0}

            for a in appts:
                if a['date']: chart_dict[a['date'].date()]['appointments'] = a['count']
            for r in reports:
                if r['date']: chart_dict[r['date'].date()]['reports'] = r['count']

            return list(chart_dict.values())

        elif timeframe == 'year':
            start_date = now.replace(month=1, day=1, hour=0, minute=0, second=0)

            # 🚀 Use direct hospital_id__in
            appts = UserAppointment.objects.filter(hospital_id__in=hospital_ids, created_at__gte=start_date) \
                .annotate(month=TruncMonth('created_at')) \
                .values('month') \
                .annotate(count=Count('id'))

            reports = UserReport.objects.filter(hospital_id__in=hospital_ids, created_at__gte=start_date) \
                .annotate(month=TruncMonth('created_at')) \
                .values('month') \
                .annotate(count=Count('id'))

            for month in range(1, 13):
                month_date = start_date.replace(month=month)
                month_str = month_date.strftime('%b') 
                chart_dict[month] = {"name": month_str, "appointments": 0, "reports": 0}

            for a in appts:
                if a['month']: chart_dict[a['month'].month]['appointments'] = a['count']
            for r in reports:
                if r['month']: chart_dict[r['month'].month]['reports'] = r['count']

            return list(chart_dict.values())

        return []