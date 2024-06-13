import openmeteo_requests
import requests
import json

file = open('params.json')
params = json.load(file)

om  = openmeteo_requests.Client()

def get_weather(location):
    output = {'temperature': 0, 'apparent_temperature': 0, 'is_day': 0, 'rain': 0, 'showers': 0, 'cloud_cover': 0, 'weather_code': 0, 'city': '', 'country': ''}

    response = requests.get(f'https://api.tomtom.com/search/2/geocode/{location}.json?key=')
    response = response.json()

    if response['results'][0]['entityType'] == 'Country': #if entityType is 'country' then the response (most likely) is just gibberish, so we handle it as 'No data found'.
        return {}

    output['city'] = response['results'][0]['address']['municipality']
    output['country'] = response['results'][0]['address']['country']

    latitude = response['results'][0]['position']['lat']
    longitude = response['results'][0]['position']['lon']

    params['latitude'] = latitude
    params['longitude'] = longitude

    responses = om.weather_api("https://api.open-meteo.com/v1/forecast", params=params)
    response = responses[0]
    current = response.Current()

    output['temperature'] = current.Variables(0).Value()
    output['humidity'] = current.Variables(1).Value()
    output['apparent_temperature'] = current.Variables(2).Value()
    output['is_day'] = current.Variables(3).Value()
    output['rain'] = current.Variables(4).Value()
    output['showers'] = current.Variables(5).Value()
    output['weather_code'] = current.Variables(6).Value()
    output['cloud_cover'] = current.Variables(7).Value()

    return output
