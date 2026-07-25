from django.urls import path
from .views import InventorySearchView, MyInventoryListCreateView, MyInventoryDetailView

urlpatterns = [
    path('search/', InventorySearchView.as_view(), name='inventory-search'),
    path('mine/', MyInventoryListCreateView.as_view(), name='inventory-mine'),
    path('mine/<int:pk>/', MyInventoryDetailView.as_view(), name='inventory-mine-detail'),
]