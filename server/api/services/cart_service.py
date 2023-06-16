from sqlalchemy import func
from api.models.cart import Cart
from api.models.cart_item import CartItem
from api.models.user import User
from api import db

def get_carts() -> list[Cart]:
    """
    Gets all carts from the database.

    :return: List of carts.
    """
    return Cart.query.all()

def get_cart(id: int) -> Cart:
    """
    Gets a cart from the database by its ID.

    :param id: ID of the cart to get.

    :return: Cart with the given ID. None if no cart exists with the given ID.
    """
    return Cart.query.get(id)

def create_cart(user_id: int) -> Cart:
    """
    Creates a cart in the database.

    :param user_id: ID of the user to create a cart for.

    :return: Cart that was created. None if no user exists with the given ID.
    """
    if not User.query.get(user_id):
        return None
    cart = Cart(user_id)
    
    db.session.add(cart)
    db.session.commit()

    return cart

def delete_cart(id: int) -> bool:
    """
    Deletes a cart from the database by its ID.

    :param id: ID of the cart to delete.

    :return: True if the cart was deleted. False if no cart exists with the given ID.
    """
    cart = Cart.query.get(id)

    if not cart:
        return False
    
    for cart_item in cart.items:
        db.session.delete(cart_item)

    db.session.delete(cart)
    db.session.commit()
    return 

def add_to_cart(cart_id: int, item_id: int, quantity: int) -> Cart:
    """
    Adds an item to a cart in the database.

    :param cart_id: ID of the cart to add the item to.
    :param item_id: ID of the item to add to the cart.
    :param quantity: Quantity of the item to add to the cart.

    :return: Cart that was updated.
    """
    # see if item is already in cart, if it is, update quantity
    cart_item = CartItem.query.filter_by(cart_id=cart_id, item_id=item_id).first()
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(cart_id, item_id, quantity)
        max_id = db.session.query(func.max(CartItem.id)).scalar()
        new_id = int(max_id) + 1 if max_id else 1
        cart_item.id = new_id

        db.session.add(cart_item)

    db.session.commit()
    return Cart.query.get(cart_id)

def remove_from_cart(cart_id: int, item_id: int) -> Cart:
    """
    Removes an item from a cart in the database.

    :param cart_id: ID of the cart to remove the item from.
    :param item_id: ID of the item to remove from the cart.

    :return: Cart that was updated.
    """
    cart_item = CartItem.query.filter_by(cart_id=cart_id, item_id=item_id).first()
    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
    return Cart.query.get(cart_id)
