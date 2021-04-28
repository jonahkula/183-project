"""
This file defines the database models
"""

import datetime
from .common import db, Field, auth
from pydal.validators import *


def get_user_email():
    return auth.current_user.get('email') if auth.current_user else None


def get_time():
    return datetime.datetime.utcnow()


# Location Table
db.define_table(
    'location',
    Field('location_name'),
    Field('location_address'),
    Field('location_phone'),
    Field('location_website'),
    Field('saved_locations_zipcode'),
    Field('saved_locations_radius'),
)

# Reviews Table
db.define_table(
    'reviews',
    Field('location_id', 'reference location'),
    Field('user_id', 'reference auth_user'),
    Field('reviews_message'),
    Field('reviews_user_rating'),
    Field('reviews_message_rating'),
    Field('reviews_threads', 'integer')
)

# Saved Locations Table
db.define_table(
    'saved_locations',
    Field('user_id', 'reference auth_user'),
    Field('location_id', 'reference location'),
    Field('saved_locations_radius'),
)


# Define your table below
#
# db.define_table('thing', Field('name'))
#
# always commit your models to avoid problems later

db.commit()
