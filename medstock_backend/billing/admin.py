from django.contrib import admin
from .models import Invoice, InvoiceItem


class InvoiceItemInline(admin.TabularInline):
    """
    Shows InvoiceItems nested INSIDE the Invoice admin page, instead of as
    a separate section. Makes sense here: nobody looks at an invoice item
    without its parent invoice for context.
    """
    model = InvoiceItem
    extra = 0
    readonly_fields = ('medicine_name', 'unit_price', 'quantity', 'line_total')
    can_delete = False


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'pharmacy', 'total_amount', 'payment_method', 'created_at')
    list_filter = ('pharmacy', 'payment_method')
    readonly_fields = ('subtotal', 'gst_amount', 'total_amount', 'created_at')
    inlines = [InvoiceItemInline]