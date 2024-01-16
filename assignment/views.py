import requests
import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    api_url = 'https://gbfs.lyft.com/gbfs/2.3/chi/en/free_bike_status.json'
    response = requests.get(api_url)
    if response.status_code == 200:
        api_data = response.json()
        bike_status_data = api_data.get('data', {}).get('bikes', [])
        tabular_data = pd.DataFrame(bike_status_data)
        num_bikes = len(bike_status_data)
        tabular_data_bikes = (tabular_data['vehicle_type_id'].astype(int) == 3).sum()
        num_disabled_bikes = tabular_data['is_disabled'].sum()
        num_reserved_bikes = tabular_data['is_reserved'].sum()
        avg_range = tabular_data['current_range_meters'].mean()

        context = {
            'tabular_data': tabular_data.to_html(),
            'num_bikes': num_bikes,
            'num_current_bikes': tabular_data_bikes,
            'num_disabled_bikes': num_disabled_bikes,
            'num_reserved_bikes': num_reserved_bikes,
            'avg_range': avg_range
        }
        return render(request, 'index.html', context)
    else:
        return HttpResponse(f'Error accessing API: {response.status_code}')
    
from django.http import JsonResponse

def refresh_data(request):
    api_url = 'https://gbfs.lyft.com/gbfs/2.3/chi/en/free_bike_status.json'
    response = requests.get(api_url)
    
    if response.status_code == 200:
        api_data = response.json()
        bike_status_data = api_data.get('data', {}).get('bikes', [])
        tabular_data = pd.DataFrame(bike_status_data)
        
        avg_range = tabular_data['current_range_meters'].mean()
        data = {'avg_range': avg_range}
        return JsonResponse(data)
    else:
        return JsonResponse({'error': f'Error accessing API: {response.status_code}'})