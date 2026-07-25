from django.contrib import admin
from .models import Inventory


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('medicine', 'pharmacy', 'quantity', 'price', 'expiry_date')
    list_filter = ('pharmacy',)
    search_fields = ('medicine__name', 'pharmacy__name')