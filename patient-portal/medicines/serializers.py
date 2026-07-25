from rest_framework import serializers
from .models import Category, Medicine


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class MedicineSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Medicine
        fields = (
            'id', 'name', 'generic_name', 'manufacturer',
            'category', 'category_name', 'requires_prescription', 'description',
        )