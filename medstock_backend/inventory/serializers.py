from rest_framework import serializers
from .models import Inventory


class InventorySerializer(serializers.ModelSerializer):
    medicine_name = serializers.CharField(source='medicine.name', read_only=True)
    pharmacy_name = serializers.CharField(source='pharmacy.name', read_only=True)
    pharmacy_city = serializers.CharField(source='pharmacy.city', read_only=True)

    class Meta:
        model = Inventory
        fields = (
            'id', 'pharmacy', 'pharmacy_name', 'pharmacy_city',
            'medicine', 'medicine_name', 'quantity', 'price',
            'batch_number', 'expiry_date', 'is_available', 'is_low_stock',
        )
        read_only_fields = ('is_available', 'is_low_stock')


class InventoryWriteSerializer(serializers.ModelSerializer):
    """
    Separate, simpler serializer for pharmacy staff adding/updating their
    OWN stock. Doesn't expose is_available/is_low_stock as those are
    computed properties, not real fields to write to.
    """
    class Meta:
        model = Inventory
        fields = ('id', 'medicine', 'quantity', 'price', 'batch_number', 'expiry_date')