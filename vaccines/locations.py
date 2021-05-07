from __future__ import annotations
import requests, pprint
from typing import List, Dict

class Location():

    def __init__(self : Location, zipcode : str, radius: str) -> None:
        self.zipcode = zipcode
        self.radius = radius

    def get_locations(self: Location) -> List[Dict[str, str]]:
        geocode = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{self.zipcode}.json?country=us&types=postcode&autocomplete=false&access_token=pk.eyJ1IjoiaGVhbHRobWFwIiwiYSI6ImNrNnYzOXA3ajAxZDkzZHBqbW1tanNuc2EifQ.HR9Av0vkGQI7FyaTtlpmdw"
        coordinates_json = requests.get(geocode).json()

        # header suggestion from: https://stackoverflow.com/questions/51154114/python-request-get-fails-to-get-an-answer-for-a-url-i-can-open-on-my-browser 
        header = {'User-Agent':"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Mobile Safari/537.36", "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}

        long, lat = coordinates_json['features'][0]['geometry']['coordinates']
        health_url = f"https://api.us.castlighthealth.com/vaccine-finder/v1/provider-locations/search?medicationGuids=779bfe52-0dd8-4023-a183-457eb100fccc,a84fb9ed-deb4-461c-b785-e17c782ef88b,784db609-dc1f-45a5-bad6-8db02e79d44f&lat={lat}&long={long}&radius={self.radius}"        

        health_json = requests.get(health_url, headers=header).json()
        return health_json['providers']

# GEOCODE_URL = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{zipcode}.json?country=us&types=postcode&autocomplete=false&access_token=pk.eyJ1IjoiaGVhbHRobWFwIiwiYSI6ImNrNnYzOXA3ajAxZDkzZHBqbW1tanNuc2EifQ.HR9Av0vkGQI7FyaTtlpmdw"
# HEALTH_URL = "https://api.us.castlighthealth.com/vaccine-finder/v1/provider-locations/search?medicationGuids=779bfe52-0dd8-4023-a183-457eb100fccc,a84fb9ed-deb4-461c-b785-e17c782ef88b,784db609-dc1f-45a5-bad6-8db02e79d44f&lat=34.18&long=-118.45&radius=25"
# # header suggestion from: https://stackoverflow.com/questions/51154114/python-request-get-fails-to-get-an-answer-for-a-url-i-can-open-on-my-browser 
# header = {'User-Agent':"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Mobile Safari/537.36", "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}
# r = requests.get(GEOCODE_URL)
# data = r.json()

# long, lat = data['features'][0]['geometry']['coordinates']
# health_url = f"https://api.us.castlighthealth.com/vaccine-finder/v1/provider-locations/search?medicationGuids=779bfe52-0dd8-4023-a183-457eb100fccc,a84fb9ed-deb4-461c-b785-e17c782ef88b,784db609-dc1f-45a5-bad6-8db02e79d44f&lat={lat}&long={long}&radius=50"

# health_request = requests.get(health_url, headers=header)
# new_data = health_request.json()
# pprint.pprint(new_data) # this data contains information about vaccine locations

# l = Location("91411", "25")
# l.parse_locations()