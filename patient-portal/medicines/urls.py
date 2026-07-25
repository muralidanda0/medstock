from django.urls import path
from .views import MedicineListView, CategoryListView

urlpatterns = [
    path('', MedicineListView.as_view(), name='medicine-list'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
]