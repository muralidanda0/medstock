from django.db import models
from pharmacies.models import Pharmacy
from medicines.models import Medicine


class Inventory(models.Model):
    """
    The per-pharmacy stock record for one medicine.

    This is the busiest table in the whole system — every invoice generated
    updates a row here, and every patient search reads from here. Every
    field and index below is chosen with that in mind.
    """
    pharmacy = models.ForeignKey(
        Pharmacy, on_delete=models.CASCADE, related_name='inventory_items'
    )
    medicine = models.ForeignKey(
        Medicine, on_delete=models.CASCADE, related_name='inventory_items'
    )

    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # DecimalField, not FloatField — money must never use floating point,
    # which can introduce rounding errors (e.g. 0.1 + 0.2 != 0.3 in float).

    batch_number = models.CharField(max_length=100, blank=True)
    expiry_date = models.DateField(null=True, blank=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # A pharmacy should only have ONE inventory row per medicine
        # (per batch, in a fuller design — simplified to one row per
        # medicine for our MVP). This constraint prevents duplicate/
        # conflicting stock rows for the same pharmacy+medicine pair.
        unique_together = ('pharmacy', 'medicine')
        indexes = [
            models.Index(fields=['pharmacy', 'medicine']),  # billing lookups
            models.Index(fields=['quantity']),               # low-stock queries
            models.Index(fields=['expiry_date']),             # near-expiry queries
        ]

    def __str__(self):
        return f"{self.medicine.name} @ {self.pharmacy.name} ({self.quantity} units)"

    @property
    def is_low_stock(self):
        # Simple placeholder threshold; we'll make this configurable later.
        return self.quantity < 10

    @property
    def is_available(self):
        return self.quantity > 0