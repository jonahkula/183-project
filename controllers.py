"""
This file defines actions, i.e. functions the URLs are mapped into
The @action(path) decorator exposed the function at URL:
    http://127.0.0.1:8000/{app_name}/{path}
If app_name == '_default' then simply
    http://127.0.0.1:8000/{path}
If path == 'index' it can be omitted:
    http://127.0.0.1:8000/
The path follows the bottlepy syntax.
@action.uses('generic.html')  indicates that the action uses the generic.html template
@action.uses(session)         indicates that the action uses the session
@action.uses(db)              indicates that the action uses the db
@action.uses(T)               indicates that the action uses the i18n & pluralization
@action.uses(auth.user)       indicates that the action requires a logged in user
@action.uses(auth)            indicates that the action requires the auth object
session, db, T, auth, and tempates are examples of Fixtures.
Warning: Fixtures MUST be declared with @action.uses({fixtures}) else your app will result in undefined behavior
"""

from __future__ import annotations
import requests, pprint
from typing import List, Dict

from py4web import action, request, abort, redirect, URL
from yatl.helpers import *
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash
from py4web.utils.url_signer import URLSigner
from .models import get_user_email
from .settings import APP_FOLDER
import os, json, pprint

url_signer = URLSigner(session)

# gets the users first name, last name, email, and saved locations


def get_user_info(db):
    user_info_dict = db(db.auth_user.email ==
                        get_user_email()).select().first()
    user_info = []
    saved_locations = []
    first_name = user_info_dict['first_name']
    last_name = user_info_dict['last_name']
    email = user_info_dict['email']
    user_id = user_info_dict['id']
    user_info.extend((first_name, last_name, email))

    saved_locations_dict = db((user_id == db.saved_location.user_id) & (
        db.saved_location.location_id == db.location.id)).select()
    print("The saved locations we found for the user is:",
          saved_locations_dict, type(saved_locations_dict))
    for saved_locations_info in saved_locations_dict:
        single_location = []
        zipcode = saved_locations_info['saved_location']['location_zipcode']
        radius = saved_locations_info['saved_location']['location_radius']
        location_name = saved_locations_info['location']['location_name']
        location_address = saved_locations_info['location']['location_address']
        print(location_name, location_address, zipcode, radius)
        single_location.extend(
            (location_name, location_address, zipcode, radius))
        print(single_location)
        saved_locations.append(single_location)

    user_info.append(saved_locations)
    return user_info


# function that saves a location to a user
def saveToUser(address, user_id):
    # Get the id of the location we just inserted
    location = db(db.location.location_address == address).select().first()

    # Insert into users saved locations
    db.saved_location.insert(
        user_id=user_id,
        location_id=location['id'],
        location_zipcode=91111,
        location_radius=0
    )


# welcome page
@action('index')
@action.uses(db, auth, 'index.html')
def index():
    return dict()


def get_saved_work():
     # Getting the id of the user
    user = db(db.auth_user.email == get_user_email()).select().first()
    user_id = user['id']

    # Getting a list of saved locations of the user
    saved = db(
        db.location.id == db.saved_location.location_id,
        db.saved_location.user_id == user_id
    ).select()

    saved_address = []
    for save in saved:
        saved_address.append(save.location.location_address)

    return saved_address


# home page
@action('main')
@action.uses(db, auth, 'content.html')
def main():
    if get_user_email() == None:
        redirect(URL('index'))

    return dict(
        add_locations_url=URL('add_locations'),
        load_home_url=URL('load_home'),
        save_url=URL('save'),
    )


@action('load_home')
def load_home():
    pass


@action('add_locations', method="POST")
@action.uses(auth)
def add_locations():
    if get_user_email() == None:
        redirect(URL('index'))
        
    l = Location(request.json.get('zipCode'), request.json.get('radius'))
    all_locations = l.get_locations()
    saved_address = get_saved_work()

    return dict(
        content=all_locations,
        saved=saved_address,
        )


# profile page
@action('profile')
@action.uses(db, auth, 'profile.html')
def profile():
    # Making sure the user is logged in.
    if get_user_email() == None:
        redirect(URL('index'))

    # Get user information
    user_info = get_user_info(db)

    return dict(
        user_info=user_info,
    )


# save a location -> currently doesn't work
@action('save', method=['GET', 'POST'])
@action.uses(db, auth)
def save():
    saved_locations = request.json.get('savedLocations')
    address = saved_locations.address1
    name = saved_locations.name

    if get_user_email() == None:
        redirect(URL('index'))

    # Get the current user id
    user = db(db.auth_user.email == get_user_email()).select().first()
    user_id = user['id']

    check = db(db.location.location_address == address).select().first()

    if (check is not None):
        saveToUser(address, user_id)
    else:
        # Inserting into location table
        db.location.insert(
            location_name=name,
            location_address=address
        )

        saveToUser(address, user_id)

    redirect(URL('main'))

    return dict()


# OLD SAVE in case you need it Wayland.

# save a location
# @action('save/<name>/<address>', method=["GET", "POST"])
# @action.uses(db, auth)
# def save(name=None, address=None):
#     assert name is not None
#     assert address is not None

#     if get_user_email() == None:
#         redirect(URL('index'))

#     # Get the current user id
#     user = db(db.auth_user.email == get_user_email()).select().first()
#     user_id = user['id']

#     check = db(db.location.location_address == address).select().first()

#     if (check is not None): 
#         saveToUser(address, user_id)
#     else:
#         # Inserting into location table
#         db.location.insert(
#             location_name = name,
#             location_address = address
#         )

#         saveToUser(address, user_id)
        
#     redirect(URL('main'))
    
#     return dict()


# unsave a location
@action('unsave/<address>', method=["GET", "POST"])
@action.uses(db, auth)
def unsave(address=None):
    assert address is not None

    if get_user_email() == None:
        redirect(URL('index'))

    # Get the current user id
    user = db(db.auth_user.email == get_user_email()).select().first()
    user_id = user['id']

    # Deleting an saved location
    location = db(db.location.location_address == address).select().first()
    unsave_location = db(
        db.saved_location.location_id == location.id,
        db.saved_location.user_id == user_id
    ).select()

    db(db.saved_location.id == unsave_location[0]['id']).delete()

    redirect(URL('main'))

    return dict()


# profile page
@action('location')
@action.uses(db, auth, 'location.html')
def location():
    # Making sure the user is logged in.
    if get_user_email() == None:
        redirect(URL('index'))

    # Get user information
    # user_info = get_user_info(db)

    rating_information = []
    rating_num = 4
    reviews_len = 14
    return dict(rating_cards1=["Pros", "Cons"],
                rating_num=rating_num,
                reviews_len=reviews_len,
                load_location_info_url = URL('location_info', signer=url_signer),
                load_review_info_url =  URL('review_info', signer=url_signer),
    )



# API for location information
# Will be hardcoded for now
@action('location_info')
@action.uses(url_signer.verify(), db)
def load_location_info():
    return dict(location_name="CVS",
                location_address="600 Front St",
                website="https://cvs.com",
                phone="123-456-7890",
            )

# API for review information
# Will be hardcoded for now
@action('review_info')
@action.uses(url_signer.verify(), db)
def load_location_info():
    return dict(review_num=54,
                review_message="I went to cvs and it was decent.",
                review_avg_num=5,
            )

# for the web scraper
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
