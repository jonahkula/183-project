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
    Field('location_zipcode'),
    Field('location_radius', 'float')
)

# Reviews Table
db.define_table(
    'review',
    Field('location_id', 'reference location'),
    Field('user_id', 'reference auth_user'),
    Field('review_message'),
    Field('review_user_rating', 'integer'),
    Field('review_message_rating', 'integer'),
    Field('review_threads', 'integer')
)

# Saved Locations Table
db.define_table(
    'saved_location',
    Field('user_id', 'reference auth_user'),
    Field('location_id', 'reference location'),
)


# Define your table below
#
# db.define_table('thing', Field('name'))
#
# always commit your models to avoid problems later

db.commit()
