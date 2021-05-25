import datetime
from .common import db, Field, auth
from pydal.validators import *

def get_user_email():
    return auth.current_user.get('email') if auth.current_user else None

def get_user():
    return auth.current_user.get('id') if auth.current_user else None

def get_time():
    return datetime.datetime.utcnow()

# Locations Table
db.define_table(
    'location',
    Field('location_name', requires=IS_NOT_EMPTY()),
    Field('location_address', requires=IS_NOT_EMPTY()),
)

# Saved Locations Table
db.define_table(
    'saved_location',
    Field('user_id', 'reference auth_user', requires=IS_NOT_EMPTY()),
    Field('location_id', 'reference location', requires=IS_NOT_EMPTY()),
    Field('location_zipcode', requires=IS_NOT_EMPTY()),
    Field('location_radius', 'float', requires=IS_NOT_EMPTY())
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
)

# Review Thread Table
db.define_table(
    'thread',
    Field('review_id', 'reference review', requires=IS_NOT_EMPTY()),
    Field('user_id', 'reference auth_user', requires=IS_NOT_EMPTY()),
    Field('thread_message', requires=IS_NOT_EMPTY()),
)

# Review Rating Table
db.define_table(
    'review_rating',
    Field('review', 'reference review'),
    Field('rating', 'integer', default=0),
    Field('rater', 'reference auth_user', default=get_user),
)

# Total Review Ratings Table
db.define_table(
    'review_raters',
    Field('review', 'reference review'),
    Field('likers', 'integer', default=0),
    Field('dislikers', 'integer', default=0),
)

db.location.id.readable = db.location.id.writable = False

db.commit()
