from django.urls import path
from .views import PharmacyCreateView, MyPharmacyView, PharmacyListView

urlpatterns = [
    path('register/', PharmacyCreateView.as_view(), name='pharmacy-register'),
    path('me/', MyPharmacyView.as_view(), name='pharmacy-me'),
    path('', PharmacyListView.as_view(), name='pharmacy-list'),
]