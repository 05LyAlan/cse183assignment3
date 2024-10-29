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

url_signer = URLSigner(session)

@action('index')
@action.uses('index.html', db, auth.user)
def index():
    return dict(
        # For example...
        load_data_url = URL('load_data'),
        add_item_url=URL('add_item'),
        update_item_url=URL('update_item'),
        delete_item_url=URL('delete_item'),
    )

@action('load_data')
@action.uses(db, auth.user)
def load_data():
    # Load items for the logged-in user
    items = db(db.shopping_list.user_email == auth.current_user.get('email')).select(
        orderby=(db.shopping_list.purchased, db.shopping_list.id)
    ).as_list()

    #items.sort(key=lambda item: (item['purchased'], item['id']))
    return dict(items=items)

@action('add_item', method='POST')
@action.uses(db, auth.user)
def add_item():
    item_name = request.json.get('item_name')
    item_id = db.shopping_list.insert(item_name=item_name, user_email=auth.current_user.get('email'), purchased=False)
    item = db.shopping_list[item_id]
    return dict(item=item.as_dict())

@action('update_item', method="POST")
@action.uses(db, auth.user)
def update_item():
    item_id = request.json.get('id')
    purchased = request.json.get('purchased')
    db(db.shopping_list.id == item_id).update(purchased=purchased)
    return "ok"

@action('delete_item', method="POST")
@action.uses(db, auth.user)
def delete_item():
    item_id = request.json.get('id')
    if item_id:
        print(f"Deleting item with ID: {item_id}")  # Debug log
        count = db(db.shopping_list.id == item_id).delete()
        if count:
            return dict(status="ok")  # Send a JSON response
    return dict(status="error")  # Send an error response