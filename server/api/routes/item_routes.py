import json
from flask import Blueprint, Response, jsonify, make_response, request 
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

@bp.route('/<int:id>/', methods=['GET'])
def get_item(id: int) -> Response:
    """
    Response to a GET request to /item/<item_id>. Gets an item from the database.

    :param id: The ID of the item to get.

    :return: Response with HTTP status of OK and the item.
    Response with HTTP status of NOT_FOUND if the item does not exist.
    """
    item = item_service.get_item(id)
    if not item:
        return make_response(jsonify({'error': 'Item not found'}), 404)
    return make_response(jsonify(item.serialize()), 200)

@bp.route('/<int:id>/', methods=['PUT'])
def update_item(id: int) -> Response:
    """
    Response to a PUT request to /item/<item_id>. Updates an item in the database.

    :param id: The ID of the item to update.
    :param item: An item object with the name, description, price, category, size, color, and stock of the item.

    :return: Response with HTTP status of OK and the updated item.
    Response with HTTP status of NOT_FOUND if the item does not exist.
    """
    data = json.loads(json.loads(request.form.get('data')))
    
    item = Item(**data)
    item = item_service.update_item(id, item)
    if not item:
        return make_response(jsonify({'error': 'Item not found'}), 404)
    return make_response(jsonify(item.serialize()), 200)

@bp.route('/<int:id>/', methods=['DELETE'])
def delete_item(id: int) -> Response:
    """
    Response to a DELETE request to /item/<item_id>. Deletes an item from the database.

    :param id: The ID of the item to delete.

    :return: Response with HTTP status of OK and the deleted item.
    Response with HTTP status of NOT_FOUND if the item does not exist.
    """
    deleted = item_service.delete_item(id)
    if not deleted:
        return make_response(jsonify({'error': 'Item not found'}), 404)
    return make_response(jsonify({'message': 'Item deleted'}), 200)

@bp.route('/image/<int:id>/', methods=['PUT'])
def update_item_image(id: int) -> Response:
    """
    Response to a PUT request to /item/image/<item_id>. Updates an item's image in the database.

    :param id: The ID of the item to update.
    :param image: An image file to upload.

    :return: Response with HTTP status of OK and the updated item.
    Response with HTTP status of NOT_FOUND if the item does not exist.
    """
    image = request.files.get('image')
    item = item_service.update_item_image(id, image)
    if not item:
        return make_response(jsonify({'error': 'Item not found'}), 404)
    return make_response(jsonify(item.serialize()), 200)
