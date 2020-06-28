from django.urls import path
from . import views

urlpatterns= [
    path('', views.index, name='index'),
    path('cars/', views.CarListView.as_view(), name="cars"),
    path('car/<int:pk>', views.CarDetailView.as_view(), name='car-detail'),
    path('car_search/', views.CarSearchForm.as_view(), name='car-search'),
    path('cars_search_results/', views.CarSearchResultsView.as_view(), name='car-search-results'),
    path('drivers/', views.DriverListView.as_view(), name="drivers"),
    path('driver/<int:pk>', views.DriverDetailView.as_view(), name="driver-detail"),
    path('driver_search/', views.DriverSearchForm.as_view(), name='driver-search'),
    path('driver_search_results/', views.DriverSearchResultsView.as_view(), name='driver-search-results'),
    path('insurance/', views.InsuranceListView.as_view(), name="insurance"),
    path('insurance/<int:pk>', views.InsuranceDetailView.as_view(), name="insurance-detail"),
    path('insurance_search/', views.InsuranceSearchForm.as_view(), name="insurance-search"),
    path('insurance_search_results/', views.InsuranceSearchResultsView.as_view(), name="insurance-search-results"),
]