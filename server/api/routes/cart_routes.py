from flask import Blueprint, Response, jsonify, make_response, request 
from api.services import cart_service, item_service

bp = Blueprint('cart', __name__, url_prefix='/cart')

@bp.route('/', methods=['GET'])
def get_carts() -> Response:
    """
    Response to a GET request to /cart. Gets all carts from the database.

    :return: Response with HTTP status of OK and a list of carts.
    """
    carts = cart_service.get_carts()
    return make_response(jsonify([cart.serialize() for cart in carts]), 200)

@bp.route('/<int:id>/', methods=['GET'])
def get_cart(id: int) -> Response:
    """
    Response to a GET request to /cart/<id>. Gets a cart from the database by its ID.

    :param id: ID of the cart to get.

    :return: Response with HTTP status of OK and the cart with the given ID.
    Response with HTTP status of NOT FOUND if no cart exists with the given ID.
    """
    cart = cart_service.get_cart(id)

    if cart is None:
        return make_response(jsonify({'error': f'Cart with id {id} not found'}), 404)

    return make_response(jsonify(cart.serialize()), 200)

@bp.route('/<int:id>/', methods=['POST'])
def create_cart(id: int) -> Response:
    """
    Response to a POST request to /cart. Creates a cart in the database.

    :return: Response with HTTP status of CREATED and the created cart.
    Response with HTTP status of BAD REQUEST if the cart already exists.
    Response with HTTP status of NOT FOUND if the user does not exist.
    """

    cart = cart_service.get_cart(id)
    if cart:
        return make_response(jsonify({'error': f'Cart with id {id} already exists'}), 400)
    
    cart = cart_service.create_cart(id)
    if not cart:
        return make_response(jsonify({'error': f'User with id {id} not found'}), 404)
    
    return make_response(jsonify(cart.serialize()), 201)

@bp.route('/<int:id>/', methods=['DELETE'])
def delete_cart(id: int) -> Response:
    """
    Response to a DELETE request to /cart/<id>. Deletes a cart from the database by its ID.

    :param id: ID of the cart to delete.

    :return: Response with HTTP status of OK and the deleted cart.
    Response with HTTP status of NOT FOUND if no cart exists with the given ID.
    """
    deleted = cart_service.delete_cart(id)

    if not deleted:
        return make_response(jsonify({'error': f'Cart with id {id} not found'}), 404)

    return make_response({'message': 'cart deleted'}, 200)

@bp.route('/item/<int:id>/', methods=['PUT'])
def add_to_cart(id: int) -> Response:
    """
    Response to a PUT request to /cart/item/<id>. Adds an item to a cart in the database.

    :param id: ID of the cart to add the item to.
    :param item_id: ID of the item to add to the cart.
    :param quantity: Quantity of the item to add to the cart.

    :return: Response with HTTP status of OK and the updated cart.
    Response with HTTP status of NOT FOUND if no cart exists with the given ID.
    Response with HTTP status of BAD REQUEST if the quantity is less than 1.
    Response with HTTP status of BAD REQUEST if the item does not exist.
    """
    data = request.get_json()
    item_id = data.get('item_id')
    quantity = data.get('quantity')
    if quantity < 1:
        return make_response(jsonify({'error': 'Quantity must be greater than 0'}), 400)
    
    # check if item exists
    item = item_service.get_item(item_id)
    if item is None:
        return make_response(jsonify({'error': f'Item with id {item_id} not found'}), 404)
    
    cart = cart_service.get_cart(id)
    if cart is None:
        return make_response(jsonify({'error': f'Cart with id {id} not found'}), 404)

    cart_item = cart_service.add_to_cart(id, item_id, quantity)
    return make_response(jsonify(cart_item.serialize()), 200)

@bp.route('/item/<int:id>/', methods=['DELETE'])
def remove_from_cart(id: int) -> Response:
    """
    Response to a DELETE request to /cart/item/<id>. Removes an item from a cart in the database.

    :param id: ID of the cart to remove the item from.
    :param item_id: ID of the item to remove from the cart.

    :return: Response with HTTP status of OK and the updated cart.
    Response with HTTP status of NOT FOUND if no cart exists with the given ID.
    Response with HTTP status of BAD REQUEST if the item does not exist.
    """
    data = request.get_json()
    item_id = data.get('item_id')

    # check if item exists
    item = item_service.get_item(item_id)
    if item is None:
        return make_response(jsonify({'error': f'Item with id {item_id} not found'}), 404)
    
    cart = cart_service.get_cart(id)
    if cart is None:
        return make_response(jsonify({'error': f'Cart with id {id} not found'}), 404)

    cart = cart_service.remove_from_cart(id, item_id)
    return make_response(jsonify(cart.serialize()), 200)
