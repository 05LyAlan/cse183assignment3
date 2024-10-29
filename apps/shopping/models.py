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

# Add here any table definition you need. Below is an example.
db.define_table('shopping_list',
    Field('item_name', 'string', requires=IS_NOT_EMPTY()),  # Item name
    Field('purchased', 'boolean', default=False),           # Purchase status
    Field('user_email', 'string', default=get_user_email)   # Associated user
)

db.commit()