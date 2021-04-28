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
from yatl.helpers import A
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash
from py4web.utils.url_signer import URLSigner
from .models import get_user_email


# Helper Functions
def get_location(location_id):
    unparsed_locations = db(db.location.id == location_id).select()
    # print(unparsed_locations['location_name'])
    # print(unparsed_locations)
    unparsed_locations
    # return db.db.location


def get_user_info(user_id):

    # Checking to make sure the user has passed a valid integer
    if type(user_id) is not int:
        print("get_userinfo: The id you have entered is not a valid integer.")
        return []
    print(type(user_id))

    # Getting the information from the database
    unparsed_userinfo = db(db.auth_user.id == user_id).select().first()
    parsed_userinfo = []
    print(unparsed_userinfo)
    if(unparsed_userinfo is None):
        print("get_userinfo: The id you have entered is not in our database")
        return []

    # Parsing the data into a list
    for i in unparsed_userinfo:
        if(i is "first_name" or i is "last_name"):
            parsed_userinfo.append(unparsed_userinfo[i])

    # Printing the values of the list
    for i in range(len(parsed_userinfo)):
        print(parsed_userinfo[i])

    return parsed_userinfo


def get_saved_locations(user_id):
    # Checking to make sure the user has passed a valid integer
    if type(user_id) is not int:
        print("get_userinfo: The id you have entered is not a valid integer.")
        return []
    print(type(user_id))

    # Getting the information from the database
    unparsed_userinfo = db((db.auth_user.id == user_id) and (
        db.saved_locations.user_id)).select().first()
    parsed_userinfo = []
    print(unparsed_userinfo)
    if(unparsed_userinfo is None):
        print("get_userinfo: The id you have entered is not in our database")
        return []


url_signer = URLSigner(session)


@action('index')
@action.uses(db, auth, 'index.html')
def index():
    return dict()


@action('sign_up')
@action.uses(db, auth, 'signup.html')
def index():
    return dict()


@action('login')
@action.uses(db, auth, 'login.html')
def index():
    return dict()


@action('forgot_password')
@action.uses(db, auth, 'password.html')
def index():
    return dict()


@action('main')
@action.uses(db, auth, 'content.html')
def index():
    return dict()


@action('profile/<user_id:int>')
@action.uses(db, auth, 'profile.html')
def index(user_id=None):

    # When authentication works, put it here
    # rows = db(db.contact.user_email == get_user_email()).select()

    # Getting First/Last Name
    # userinfo[0] = First name
    # userinfo[1] = Last name
    userinfo = get_user_info(user_id)

    # Getting Saved Locations
    saved_locations = get_saved_locations

    return dict()
