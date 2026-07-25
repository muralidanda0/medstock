from rest_framework import generics, permissions
from .models import Pharmacy
from .serializers import PharmacySerializer
from accounts.permissions import IsPharmacyRole


class PharmacyCreateView(generics.CreateAPIView):
    """
    POST /api/pharmacies/register/
    A logged-in PHARMACY-role user registers their business.
    """
    serializer_class = PharmacySerializer
    permission_classes = [permissions.IsAuthenticated, IsPharmacyRole]

    def perform_create(self, serializer):
        # owner is set from the logged-in user, NEVER trusted from the
        # request body — otherwise anyone could register a pharmacy
        # "owned" by someone else.
        serializer.save(owner=self.request.user)


class MyPharmacyView(generics.RetrieveUpdateAPIView):
    """
    GET/PATCH /api/pharmacies/me/
    A pharmacy user views/edits their own pharmacy profile.
    """
    serializer_class = PharmacySerializer
    permission_classes = [permissions.IsAuthenticated, IsPharmacyRole]

    def get_object(self):
        return self.request.user.pharmacy  # uses the related_name='pharmacy' we set earlier


class PharmacyListView(generics.ListAPIView):
    """
    GET /api/pharmacies/  — public list, e.g. for 'nearby pharmacies'.
    Only shows VERIFIED pharmacies to the outside world.
    """
    serializer_class = PharmacySerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Pharmacy.objects.filter(verification_status=Pharmacy.VerificationStatus.VERIFIED)