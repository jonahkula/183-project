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
    Field('location_name', requires=IS_NOT_EMPTY()),
    Field('location_address', requires=IS_NOT_EMPTY()),
)

# Reviews Table
db.define_table(
    'review',
    Field('location_id', 'reference location', requires=IS_NOT_EMPTY()),
    Field('user_id', 'reference auth_user', requires=IS_NOT_EMPTY()),
    Field('review_message', requires=IS_NOT_EMPTY()),
    Field('wait_time', requires=IS_NOT_EMPTY()),
    Field('service', requires=IS_NOT_EMPTY()),
    Field('title', requires=IS_NOT_EMPTY()),
    Field('vaccine', requires=IS_NOT_EMPTY()),
    Field('review_user_rating', 'integer', requires=IS_NOT_EMPTY()),
    Field('review_message_rating', 'integer', requires=IS_NOT_EMPTY()),
)

# Saved Locations Table
db.define_table(
    'saved_location',
    Field('user_id', 'reference auth_user', requires=IS_NOT_EMPTY()),
    Field('location_id', 'reference location', requires=IS_NOT_EMPTY()),
    Field('location_zipcode', requires=IS_NOT_EMPTY()),
    Field('location_radius', 'float', requires=IS_NOT_EMPTY())
)

# Review Threads Table
db.define_table(
    'thread',
    Field('user_id', 'reference auth_user', requires=IS_NOT_EMPTY()),
    Field('review_id', 'reference review', requires=IS_NOT_EMPTY()),
    Field('message', requires=IS_NOT_EMPTY())
)

db.commit()
