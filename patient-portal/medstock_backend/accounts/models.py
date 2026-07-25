from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User model extending Django's built-in AbstractUser.
    We only ADD what MedStock needs: a `role` field.
    """

    class Role(models.TextChoices):
        PATIENT = 'PATIENT', 'Patient'
        PHARMACY = 'PHARMACY', 'Pharmacy Staff'
        ADMIN = 'ADMIN', 'Platform Admin'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.PATIENT,
    )

    phone_number = models.CharField(max_length=15, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} ({self.role})"