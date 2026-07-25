from django.core.cache import cache
from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import Inventory
from .serializers import InventorySerializer, InventoryWriteSerializer
from accounts.permissions import IsPharmacyRole


class InventorySearchView(generics.ListAPIView):
    """
    GET /api/inventory/search/?medicine=paracetamol&city=Hyderabad
    Public. This is the main patient-facing search endpoint — now cached.
    """
    serializer_class = InventorySerializer
    permission_classes = [permissions.AllowAny]

    def list(self, request, *args, **kwargs):
        medicine_name = request.query_params.get('medicine', '')
        city = request.query_params.get('city', '')

        cache_key = f"inventory_search:{medicine_name.lower()}:{city.lower()}"

        cached_data = cache.get(cache_key)
        if cached_data is not None:
            print(f"CACHE HIT for key: {cache_key}")
            return Response(cached_data)

        print(f"CACHE MISS for key: {cache_key} — querying database")
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        cache.set(cache_key, serializer.data, timeout=30)

        return Response(serializer.data)

    def get_queryset(self):
        qs = Inventory.objects.select_related('medicine', 'pharmacy').filter(quantity__gt=0)

        medicine_name = self.request.query_params.get('medicine')
        if medicine_name:
            qs = qs.filter(medicine__name__icontains=medicine_name)

        city = self.request.query_params.get('city')
        if city:
            qs = qs.filter(pharmacy__city__icontains=city)

        return qs.order_by('price')


class MyInventoryListCreateView(generics.ListCreateAPIView):
    """
    GET/POST /api/inventory/mine/
    A pharmacy user views/adds stock for THEIR OWN pharmacy only.
    """
    permission_classes = [permissions.IsAuthenticated, IsPharmacyRole]

    def get_serializer_class(self):
        return InventoryWriteSerializer if self.request.method == 'POST' else InventorySerializer

    def get_queryset(self):
        return Inventory.objects.filter(pharmacy=self.request.user.pharmacy)

    def perform_create(self, serializer):
        serializer.save(pharmacy=self.request.user.pharmacy)


class MyInventoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET/PATCH/DELETE /api/inventory/mine/<id>/
    """
    serializer_class = InventoryWriteSerializer
    permission_classes = [permissions.IsAuthenticated, IsPharmacyRole]

    def get_queryset(self):
        return Inventory.objects.filter(pharmacy=self.request.user.pharmacy)