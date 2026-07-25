from rest_framework import permissions


class IsPharmacyRole(permissions.BasePermission):
    """
    Only lets through users whose `role` is PHARMACY. Used on endpoints
    like 'add inventory' or 'generate invoice' — a patient should never
    be able to hit these, even if they're logged in.
    """
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.role == request.user.Role.PHARMACY
        )


class IsOwnerPharmacy(permissions.BasePermission):
    """
    Object-level check: does this logged-in pharmacy user actually OWN
    the specific Pharmacy/Inventory row they're trying to edit? Prevents
    Pharmacy A from editing Pharmacy B's stock just because both are
    role=PHARMACY.
    """
    def has_object_permission(self, request, view, obj):
        # obj might be a Pharmacy, or something with a .pharmacy FK
        pharmacy = obj if hasattr(obj, 'owner') else obj.pharmacy
        return pharmacy.owner_id == request.user.id