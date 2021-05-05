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

from .settings import APP_FOLDER
import os
import json
JSON_FILE = os.path.join(APP_FOLDER, "static", "assets", "sample.json")

url_signer = URLSigner(session)

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

    # Sample data of locations
    results = {}
    results = json.load(open(JSON_FILE))

    # Getting the id of the user
    user = db(db.auth_user.email == get_user_email()).select().first()
    user_id = user['id']

    # Getting a list of saved 
    saved = db(db.saved_location.user_id == user_id).select()

    return dict(rows=results)

# profile page
@action('profile')
@action.uses(db, auth, 'profile.html')
def profile():
    if get_user_email() == None:
        redirect(URL('index'))
    return dict()

# Save a location
@action('save/<name>/<address>', method=["GET", "POST"])
@action.uses(db, auth)
def save(name=None, address=None):
    assert name is not None
    assert address is not None

    if get_user_email() == None:
        redirect(URL('index'))

    user = db(db.auth_user.email == get_user_email()).select().first()
    user_id = user['id']

    db.location.insert(
        location_name = name,
        location_address = address
    )

    location = db(db.location.location_address == address).select().first()

    db.saved_location.insert(
        user_id = user_id,
        location_id = location['id'],
        location_zipcode = 91111,
        location_radius = 0
    )
    redirect(URL('index'))
    
    return dict()
