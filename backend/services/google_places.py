from pprint import pprint

import requests
from django.conf import settings


def search_places(latitude, longitude):
    api_key = settings.GOOGLE_API_KEY
    location = f'{latitude},{longitude}'
    radius = 1500  # Meters
    type = 'restaurant'  # https://developers.google.com/places/web-service/supported_types
    # More parameters https://developers.google.com/places/web-service/search

    # TODO: Get some suggestions!
    url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location}&radius={radius}&type={type}&key={api_key}'
    response = requests.get(url)

    suggestions = response.json()['results']

    return suggestions
