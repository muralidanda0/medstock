from rest_framework import serializers
from .models import Pharmacy


class PharmacySerializer(serializers.ModelSerializer):
    class Meta:
        model = Pharmacy
        fields = (
            'id', 'name', 'license_number', 'address', 'city',
            'latitude', 'longitude', 'verification_status', 'created_at',
        )
        # verification_status should only be changed by an ADMIN via the
        # Django admin panel for now, not by the pharmacy itself.
        read_only_fields = ('verification_status',)