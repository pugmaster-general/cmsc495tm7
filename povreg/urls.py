from django.urls import path
from . import views

urlpatterns= [
    path('', views.index, name='index'),
    path('cars/', views.CarListView.as_view(), name="cars"),
    path('car/<int:pk>', views.CarDetailView.as_view(), name='car-detail'),
    path('cars_search/', views.CarSearchResultsView.as_view(), name='car_search_results'),
    path('drivers/', views.DriverListView.as_view(), name="drivers"),
    path('driver/<int:pk>', views.DriverDetailView.as_view(), name="driver-detail"),
    path('insurance/', views.InsuranceListView.as_view(), name="insurance"),
    path('insurance/<int:pk>', views.InsuranceDetailView.as_view(), name="insurance-detail"),
]