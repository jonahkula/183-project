import random, requests, pprint

# using military time
START_TIME = 0 
END_TIME = 24
MAX_SEC = 59

MAX_TIMES = 11

GEOCODE_URL = "https://api.mapbox.com/geocoding/v5/mapbox.places/91411.json?country=us&types=postcode&autocomplete=false&access_token=pk.eyJ1IjoiaGVhbHRobWFwIiwiYSI6ImNrNnYzOXA3ajAxZDkzZHBqbW1tanNuc2EifQ.HR9Av0vkGQI7FyaTtlpmdw"
HEALTH_URL = "https://api.us.castlighthealth.com/vaccine-finder/v1/provider-locations/search?medicationGuids=779bfe52-0dd8-4023-a183-457eb100fccc,a84fb9ed-deb4-461c-b785-e17c782ef88b,784db609-dc1f-45a5-bad6-8db02e79d44f&lat=34.18&long=-118.45&radius=25"
# header suggestion from: https://stackoverflow.com/questions/51154114/python-request-get-fails-to-get-an-answer-for-a-url-i-can-open-on-my-browser 
header = {'User-Agent':"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Mobile Safari/537.36", "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}
r = requests.get(GEOCODE_URL)
data = r.json()

# print(r.headers)
# pprint.pprint(data)
long, lat = data['features'][0]['geometry']['coordinates']
health_url = f"https://api.us.castlighthealth.com/vaccine-finder/v1/provider-locations/search?medicationGuids=779bfe52-0dd8-4023-a183-457eb100fccc,a84fb9ed-deb4-461c-b785-e17c782ef88b,784db609-dc1f-45a5-bad6-8db02e79d44f&lat={lat}&long={long}&radius=50"
# # https://api.us.castlighthealth.com/vaccine-finder/v1/provider-locations/search?medicationGuids=779bfe52-0dd8-4023-a183-457eb100fccc,a84fb9ed-deb4-461c-b785-e17c782ef88b,784db609-dc1f-45a5-bad6-8db02e79d44f&lat=34.18&long=-118.45&radius=25
# # pprint.pprint(data['features'][0]['geometry']['coordinates'])
# print(health_url, long, lat)
new_r = requests.get(health_url, headers=header)
new_data = new_r.json()
pprint.pprint(new_data)
print("new_data len: ", len(new_data['providers']))
current_location_times = []
all_times = []
for _ in range(len(new_data['providers'])):
    num_times = random.randrange(1, MAX_TIMES)
    while len(current_location_times) < num_times:
        hour = random.randrange(START_TIME, END_TIME)
        minute = random.randrange(START_TIME, MAX_SEC) if hour != END_TIME else 0
        time = "%d:%02.f " % (hour % 12 if hour > 12 else hour, minute)
        time += "A.M." if hour <= 12 else "P.M."
        if time not in current_location_times:
            current_location_times.append(time) 
    all_times.append(current_location_times)
    current_location_times = []

pprint.pprint(all_times)