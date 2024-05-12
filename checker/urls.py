from django.urls import path
from .views import index, calculate_energy_api, calculate_solar_setup
urlpatterns = [
    path('', index), 
    path('api/calculate_energy/', calculate_energy_api, name='calculate_energy_api'),
    path('api/calculate_solar_setup/', calculate_solar_setup, name='calculate_solar_setup')
]