from django.contrib import admin
from .models import (
    Claim, InsuranceProvider, TpaProvider, 
    ClaimDiagnosis, ClaimProcedure, ClaimLabOrder
)

@admin.register(Claim)
class ClaimAdminConfig(admin.ModelAdmin):
    list_display = ('id', 'nhcx_claim_id', 'hospital', 'clinical_status', 'adminal_status', 'created_at')
    search_fields = ('nhcx_claim_id', 'id', 'patient_name')
    list_filter = ('clinical_status', 'adminal_status', 'is_mlc', 'is_maternity')

admin.site.register(InsuranceProvider)
admin.site.register(TpaProvider)
admin.site.register(ClaimDiagnosis)
admin.site.register(ClaimProcedure)
admin.site.register(ClaimLabOrder)