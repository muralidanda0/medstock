from rest_framework import generics, permissions
from .models import Inventory
from .serializers import InventorySerializer, InventoryWriteSerializer
from accounts.permissions import IsPharmacyRole


class InventorySearchView(generics.ListAPIView):
    """
    GET /api/inventory/search/?medicine=paracetamol&city=Hyderabad
    Public. This is the main patient-facing search endpoint.
    """
    serializer_class = InventorySerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = Inventory.objects.select_related('medicine', 'pharmacy').filter(quantity__gt=0)

        medicine_name = self.request.query_params.get('medicine')
        if medicine_name:
            qs = qs.filter(medicine__name__icontains=medicine_name)

        city = self.request.query_params.get('city')
        if city:
            qs = qs.filter(pharmacy__city__icontains=city)

        # WHY order_by price here: simplest possible "lowest price first"
        # sort for now. Full ranking (price + distance + availability
        # weighted together) comes later once we add geolocation distance
        # calculation — flagged in your original spec as a dedicated topic.
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
        # Same principle as pharmacy ownership earlier: pharmacy is taken
        # from the logged-in user's own Pharmacy, never from request data.
        serializer.save(pharmacy=self.request.user.pharmacy)


class MyInventoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET/PATCH/DELETE /api/inventory/mine/<id>/
    """
    serializer_class = InventoryWriteSerializer
    permission_classes = [permissions.IsAuthenticated, IsPharmacyRole]

    def get_queryset(self):
        # Scoping the queryset to the logged-in pharmacy is what actually
        # prevents Pharmacy A from editing Pharmacy B's stock via this
        # endpoint — even if they guessed another pharmacy's inventory ID.
        return Inventory.objects.filter(pharmacy=self.request.user.pharmacy)