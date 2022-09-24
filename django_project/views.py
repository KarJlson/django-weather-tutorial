import os
from django.shortcuts import render
from django.http import JsonResponse
import requests

# Create your views here.
def home(request):
    return render(request, 'index.html')


def get_location_from_ip(ip_address):
    response = requests.get("http://ip-api.com/json/{}".format(ip_address))
    return response.json()

def get_weather_from_ip(request):
  ip_address = request.GET.get("ip")
  location = get_location_from_ip(ip_address)
  testcity = location.get("city")
  if testcity == 'St Petersburg':
          city = 'Saint Petersburg'
  else: city = testcity
  country_code = location.get("countryCode")
  weather_data = get_weather_from_location(city, country_code)
  description = weather_data['weather'][0]['description']
  temperature = weather_data['main']['temp']
  s = "You're in {}, {}. You can expect {} with a temperature of {} degrees".format(city, country_code, description, temperature)
  data = {"weather_data": s}
  return JsonResponse(data)


def get_weather_from_location(city, country_code):
    token = os.environ['OPEN_WEATHER_TOKEN']
    url = "https://api.openweathermap.org/data/2.5/weather?q={},{}&units=metric&appid={}".format(
        city, country_code, token)
    response = requests.get(url)
    print(url)
    return response.json()