from django.db import models


class Category(models.Model):
    """
    Medicine category, e.g. 'Painkiller', 'Antibiotic', 'Antacid'.
    Kept as its own table (not a plain CharField on Medicine) so we can:
    - filter/search by category cleanly
    - avoid typos ('Antibiotic' vs 'antibiotics' vs 'Anti-biotic')
    - let admins manage the category list without touching code
    """
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Medicine(models.Model):
    """
    The SHARED master catalog entry for a medicine — e.g. 'Paracetamol 500mg'.

    IMPORTANT DESIGN DECISION: this table does NOT hold stock quantity or
    price. Those differ PER PHARMACY (Pharmacy A might have 200 units at
    ₹20, Pharmacy B might have 0 units at ₹18). Mixing per-pharmacy data
    into this table would mean duplicating "Paracetamol 500mg" once per
    pharmacy that stocks it — a normalization violation. Instead:

        Medicine (1) ----- (many) Inventory (many) ----- (1) Pharmacy

    Medicine = "what is this drug" (shared, one row per drug)
    Inventory = "who has it, how much, at what price" (one row per
                 pharmacy-medicine pair) — defined in inventory/models.py
    """
    name = models.CharField(max_length=255)
    generic_name = models.CharField(max_length=255, blank=True)
    manufacturer = models.CharField(max_length=255, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name='medicines'
    )
    requires_prescription = models.BooleanField(default=False)
    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=['name']),          # search by name is the #1 query
            models.Index(fields=['generic_name']),  # search by generic name too
        ]