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

from py4web import action, request, abort, redirect, URL
from yatl.helpers import *
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash
from py4web.utils.url_signer import URLSigner
from .models import get_user_email

url_signer = URLSigner(session)


# Gets the users first name, last name, email, and saved locations
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

 # welcome page


@action('index')
@action.uses(db, auth, 'index.html')
def index():
    return dict()

# home page


@action('main')
@action.uses(db, auth, 'content.html')
def main():
    if get_user_email() == None:
        redirect(URL('index'))
    return dict()

# profile page


@action('profile')
@action.uses(db, auth, 'profile.html')
def profile():

    # Making sure the user is logged in.
    if get_user_email() == None:
        redirect(URL('index'))

    # Get user information
    user_info = get_user_info(db)

    return dict(user_info=user_info)
