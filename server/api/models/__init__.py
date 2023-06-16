from .user import User
from .item import Item
from .cart import Cart
from .cart_item import CartItem
from sqlalchemy import event

event.listen(User, 'before_update', User.update_timestamp)
event.listen(Item, 'before_update', Item.update_timestamp)
event.listen(Cart, 'before_update', Cart.update_timestamp)
event.listen(CartItem, 'before_update', CartItem.update_timestamp)
