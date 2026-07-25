from django.contrib import admin
from .models import Pharmacy


@admin.register(Pharmacy)
class PharmacyAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'verification_status', 'owner')
    list_filter = ('verification_status', 'city')
    search_fields = ('name', 'license_number')