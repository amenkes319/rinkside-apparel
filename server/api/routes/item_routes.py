import json
from flask import Blueprint, Response, abort, jsonify, make_response, request 
from api.services import item_service
from api.models.item import Item

bp = Blueprint('item', __name__, url_prefix='/item')

@bp.route('/', methods=['GET'])
def get_items() -> Response:
    """
    Response to a GET request to /item. Gets all items from the database.

    :return: Response with HTTP status of OK and a list of items.
    """
    items = item_service.get_items()
    return make_response(jsonify([item.serialize() for item in items]), 200)

@bp.route('/', methods=['POST'])
def create_item() -> Response:
    """
    Response to a POST request to /item. Creates an item in the database.

    :param item: An item object with the name, description, price, image_url, category, size, color, and stock of the new item.
    :param image: An image file to upload.

    :return: Response with HTTP status of CREATED and the created item.
    Response with HTTP status of CONFLICT if the item name already exists.
    """
    data = json.loads(json.loads(request.form.get('data')))
    image = request.files.get('image')
    
    item = Item(**data)
    item = item_service.create_item(item, image)
    if not item:
        return make_response(jsonify({'error': 'Item already exists'}), 409)
    return make_response(jsonify(item.serialize()), 201)