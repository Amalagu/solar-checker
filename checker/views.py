from django.shortcuts import render

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
# Create your views here.

""" 
number of panels = (Total daily energy consumption)/(panel wattage x peak sun hour)

Batteries: To have a full day’s backup, you would need batteries that can store at
 least as much as your daily consumption. For 4.1 kWh of daily consumption, you would
   need batteries that can store at least 4.1 kWh. It’s also wise to have some extra 
   capacity to account for days with less sunlight or higher usage, so you might 
   consider a system with around 6 kWh of storage.

We'll assume 300W panels and 5 peak sun hours, batteries of 10 kwh

fridge = 2 kwh/day
bulb = 0.5 kwh
laptop = 0.75 kwh

 """
def index(request):
    return render(request, 'index.html')




@csrf_exempt
@require_http_methods(["POST"])
def calculate_energy_api(request):
    # Initialize total energy consumption
    total_energy_consumption = 0

    # List of appliances from the form
    appliances = ['refrigerator', 'bulb', 'laptop', 'television', 'fan']

    # Calculate total energy consumption
    for appliance in appliances:
        if appliance in request.POST:
            amount = int(request.POST.get(f'{appliance}-amt', 0)) or 0
            load = int(request.POST.get(f'{appliance}-load', 0)) or 0
            hours = int(request.POST.get(f'{appliance}-hours', 0)) or 0
            total_energy_consumption += amount * load * hours / 1000  # Convert to kWh

    # Constants
    panel_wattage = 300  # in Watts
    battery_capacity = 10  # in kWh
    peak_sun_hours = 4  # average peak sun hours per day

    # Calculate the number of solar panels needed
    panels_needed = total_energy_consumption / (panel_wattage / 1000 * peak_sun_hours)

    # Calculate the number of batteries needed
    batteries_needed = total_energy_consumption / battery_capacity

    # Round up to the nearest whole number since you can't have a fraction of a panel or battery
    panels_needed = int(panels_needed) + (panels_needed % 1 > 0)
    batteries_needed = int(batteries_needed) + (batteries_needed % 1 > 0)

    # Prepare the JSON response
    response_data = {
        'total_daily_energy_consumption_kWh': total_energy_consumption,
        'number_of_solar_panels_needed': panels_needed,
        'number_of_batteries_needed': batteries_needed
    }
    return JsonResponse(response_data)




@csrf_exempt
@require_http_methods(["POST"])
def calculate_solar_setup(request):
    try:
        # Extract the average power consumption per day from the POST data
        power_consumption = float(request.POST.get('power-consumption', 0))

        # Constants
        panel_wattage = 300  # in Watts
        battery_capacity = 10  # in kWh
        peak_sun_hours = 4  # average peak sun hours per day

        # Calculate the number of solar panels needed
        panels_needed = power_consumption / (panel_wattage / 1000 * peak_sun_hours)

        # Calculate the number of batteries needed
        batteries_needed = power_consumption / battery_capacity

        # Round up to the nearest whole number
        panels_needed = int(panels_needed) + (panels_needed % 1 > 0)
        batteries_needed = int(batteries_needed) + (batteries_needed % 1 > 0)

        # Prepare the JSON response
        response_data = {
            'total_daily_energy_consumption_kWh': power_consumption,
            'number_of_solar_panels_needed': panels_needed,
            'number_of_batteries_needed': batteries_needed
        }

        return JsonResponse(response_data)
    except ValueError:
        return JsonResponse({'error': 'Invalid input'}, status=400)

# Add the URL pattern for this view in your urls.py:
# path('api/calculate_solar_setup/', views.calculate_solar_setup, name='calculate_solar_setup')
