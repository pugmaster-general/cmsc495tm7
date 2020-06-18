from django.urls import path
from . import views

urlpatterns= [
    path('', views.index, name='index'),
    path('cars/', views.CarListView.as_view(), name="cars"),
    path('car/<int:pk>', views.CarDetailView.as_view(), name='car-detail')
]