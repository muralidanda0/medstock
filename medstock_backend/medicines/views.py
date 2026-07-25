from rest_framework import generics, permissions, filters
from .models import Medicine, Category
from .serializers import MedicineSerializer, CategorySerializer


class MedicineListView(generics.ListAPIView):
    """
    GET /api/medicines/?search=paracetamol
    Public — anyone (even logged-out patients) can browse the catalog.
    """
    queryset = Medicine.objects.select_related('category').all()
    serializer_class = MedicineSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'generic_name', 'manufacturer']


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]