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
import requests
from typing import List, Dict
from py4web import action, request, abort, redirect, URL
from yatl.helpers import *
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash
from py4web.utils.url_signer import URLSigner
from .models import get_user_email
from .settings import APP_FOLDER
from .models import get_user

url_signer = URLSigner(session)

# clean reset of review data
@action('reset-reviews')
@action.uses(db)
def setup():
    db(db.review).delete()
    db(db.thread).delete()
    return "reviews reset, head back to home"


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
    # print("The saved locations we found for the user is:",
    #       saved_locations_dict, type(saved_locations_dict))
    for saved_locations_info in saved_locations_dict:
        single_location = []
        zipcode = saved_locations_info['saved_location']['location_zipcode']
        radius = saved_locations_info['saved_location']['location_radius']
        location_name = saved_locations_info['location']['location_name']
        location_address = saved_locations_info['location']['location_address']
        # print(location_name, location_address, zipcode, radius)
        single_location.extend(
            (location_name, location_address, zipcode, radius))
        # print(single_location)
        saved_locations.append(single_location)

    user_info.append(saved_locations)
    return user_info


# saves a location to a user
def saveToUser(address, zipCode, radius, user_id):
    # Get the id of the location we just inserted
    location = db(db.location.location_address == address).select().first()

    # Insert into users saved locations
    db.saved_location.insert(
        user_id=user_id,
        location_id=location['id'],
        location_zipcode=zipCode,
        location_radius=radius
    )


# welcome page
@action('index')
@action.uses(db, auth, 'index.html')
def index():
    return dict()


# get saved locations of a user
def get_saved_work():
    # Getting the id of the user
    user = db(db.auth_user.email == get_user_email()).select().first()
    user_id = user['id']

    # Getting a list of saved locations of the user
    saved = db(
        (db.location.id == db.saved_location.location_id) &
        (db.saved_location.user_id == user_id)
    ).select()

    saved_address = []
    for save in saved:
        saved_address.append(save.location.location_address)

    return saved_address


# load saved locations of a user
@action('load_saved', method='GET')
@action.uses(auth)
def load_saved():
    saved_address = get_saved_work()
    return dict(saved=saved_address)


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
        unsave_url=URL('unsave'),
        load_saved_url=URL('load_saved'),
    )


# load home
@action('load_home')
def load_home():
    pass


# locations for content page
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
        load_user_info_url=URL('load_user_info', signer=url_signer),
    )


# return user info
@action('load_user_info', method=['GET'])
@action.uses(db, auth)
def load_user_info():
    user_info = get_user_info(db)
    return dict(user_info=user_info)


# save a location
@action('save', method=['POST'])
@action.uses(db, auth)
def save():
    location_data = request.json.get('address')
    zipCode = request.json.get('zipCode')
    radius = request.json.get('radius')

    address = location_data['address1']
    name = location_data['name']

    if get_user_email() == None:
        redirect(URL('index'))

    # Get the current user id
    user = db(db.auth_user.email == get_user_email()).select().first()
    user_id = user['id']

    # check is used to determine if the location is already added into the locations db
    check = db(db.location.location_address == address).select().first()

    if (check is not None):
        saveToUser(address, zipCode, radius, user_id)
    else:
        # Inserting into location table
        db.location.insert(
            location_name=name,
            location_address=address
        )
        saveToUser(address, zipCode, radius, user_id)

    saved_address = get_saved_work()
    # print(saved_address)
    redirect(URL('main'))
    return dict()


# unsave a location
@action('unsave', method=["GET", "POST"])
@action.uses(db, auth)
def unsave():
    location_data = request.json.get('address')
    address = location_data['address1']

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

    saved_address = get_saved_work()
    # print(saved_address)
    redirect(URL('main'))
    return dict()


# add a review to a location
@action('add_review', method=["POST"])
@action.uses(db, auth)
def add_review():
    text = request.json.get('text')
    wait = request.json.get('wait')
    service = request.json.get('service')
    vaccine = request.json.get('vaccine')
    title = request.json.get('title')
    address = request.json.get('address')
    location_name = request.json.get('location_name')

    user = db(db.auth_user.email == get_user_email()).select().first()
    name = user.first_name + " " + user.last_name

    # Getting the location of the post that we want to add a review to
    location = db(db.location.location_address == address).select().first()

    # Check if there exists a location field
    if (location is None):
        location = db.location.insert(
            location_address = address,
            location_name = location_name,
        )

    id = db.review.insert(
        location_id = location['id'],
        user_id = user['id'],
        review_message = text,
        wait_time = wait,
        service = service,
        title = title,
        vaccine = vaccine,
        review_user_rating = 4,
        review_message_rating = 5,
    )

    return dict(name=name, id=id)


# load reviews
@action('load_review', method=["GET"])
@action.uses(db, auth)
def load_review():
    address = request.params.get('address')
    location = db(db.location.location_address == address).select().first()
    reviews = db(db.review.location_id == location['id']).select().as_list()
    return dict(reviews = reviews)


# used to get name of user
@action('get_name', method=["GET"])
@action.uses(db, auth)
def get_name():
    review_id = request.params.get('id')
    review = db(db.review.id == review_id).select().first()
    user = db(db.auth_user.id == review['user_id']).select().first()
    name = user['first_name'] + " " + user['last_name']
    return dict(name=name)


# get rating of review
@action('get_review_rating')
@action.uses(url_signer.verify(), db, auth.user)
def get_review_rating():
    review_id = request.params.get('review_id')
    row = db((db.review_rating.review == review_id) &
             (db.review_rating.rater == get_user())).select().first()
    rating = row.rating if row is not None else 0
    return dict(rating=rating)


# set rating of review
@action('set_review_rating', method='POST')
@action.uses(url_signer.verify(), db, auth.user)
def set_review_rating():
    review_id = request.json.get('review_id')
    rating = request.json.get('rating')
    assert review_id is not None and rating is not None
    db.review_rating.update_or_insert(
        ((db.review_rating.review == review_id) & (db.review_rating.rater == get_user())),
        review=review_id,
        rater=get_user(),
        rating=rating,
    )
    return "review rating set"


# get raters of a review
@action('get_review_raters')
@action.uses(url_signer.verify(), db, auth.user)
def get_review_raters():
    review_id = request.params.get('review_id')
    row = db((db.review_raters.review == review_id)).select().first()
    likers = row.likers if row is not None else 0
    dislikers = row.dislikers if row is not None else 0
    return dict(likers=likers, dislikers=dislikers)


# set raters of review
@action('set_review_raters', method='POST')
@action.uses(url_signer.verify(), db, auth.user)
def set_review_raters():
    review_id = request.json.get('review_id')
    likers = request.json.get('likers')
    dislikers = request.json.get('dislikers')
    assert review_id is not None and likers is not None and dislikers is not None
    db.review_raters.update_or_insert(
        ((db.review_raters.review == review_id)),
        review=review_id,
        likers=likers,
        dislikers=dislikers,
    )
    return "review raters set"


# location page
@action('location')
@action.uses(db, auth, 'location.html')
def location():
    # Making sure the user is logged in.
    if get_user_email() == None:
        redirect(URL('index'))

    # Using the information of the user to find the information of the location
    zipcode = request.params.get('zip')
    radius = request.params.get('rad')
    saved_location = request.params.get('loc')
    saved_address = request.params.get('addr')
    # print(zipcode, radius, saved_location, saved_address)

    # We use the zipcode and radius to find the information on a single saved_location
    location_info = extract_location_info(zipcode, radius, saved_location)
    # This occurs if a bug happens.
    # This code should never be exectued
    if location_info == None:
        redirect(URL('index'))

    rating_information = []
    rating_num = 4
    reviews_len = 14
    return dict(rating_num=rating_num,
                reviews_len=reviews_len,
                load_location_info_url = URL('location_info', signer=url_signer),
                add_review_url = URL('add_review'),
                load_review_url = URL('load_review'),
                get_name_url = URL('get_name'),
                location_info = location_info,
                get_review_rating_url = URL('get_review_rating', signer=url_signer),
                set_review_rating_url = URL('set_review_rating', signer=url_signer),
                get_review_raters_url = URL('get_review_raters', signer=url_signer),
                set_review_raters_url = URL('set_review_raters', signer=url_signer),
                )


# finds the info of a location given the zipcode, radius, and target
def extract_location_info(zipcode, radius, location_target):
    l = Location(zipcode, radius)
    all_locations = l.get_locations()
    for location in all_locations:
        if location['name'] == location_target:
            return location
    return None


# for the web scraper
class Location():
    def __init__(self: Location, zipcode: str, radius: str) -> None:
        self.zipcode = zipcode
        self.radius = radius

    def get_locations(self: Location) -> List[Dict[str, str]]:
        geocode = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{self.zipcode}.json?country=us&types=postcode&autocomplete=false&access_token=pk.eyJ1IjoiaGVhbHRobWFwIiwiYSI6ImNrNnYzOXA3ajAxZDkzZHBqbW1tanNuc2EifQ.HR9Av0vkGQI7FyaTtlpmdw"
        coordinates_json = requests.get(geocode).json()

        # header suggestion from: https://stackoverflow.com/questions/51154114/python-request-get-fails-to-get-an-answer-for-a-url-i-can-open-on-my-browser
        header = {'User-Agent': "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Mobile Safari/537.36", "Upgrade-Insecure-Requests": "1",
                  "DNT": "1", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate"}

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
