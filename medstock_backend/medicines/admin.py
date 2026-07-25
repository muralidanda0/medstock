from django.contrib import admin
from .models import Category, Medicine


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('name',)


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('name', 'generic_name', 'manufacturer', 'category', 'requires_prescription')
    list_filter = ('category', 'requires_prescription')
    search_fields = ('name', 'generic_name', 'manufacturer')