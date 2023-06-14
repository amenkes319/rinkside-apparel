from .user import User
from .item import Item
from sqlalchemy import event

event.listen(User, 'before_update', User.update_timestamp)
event.listen(Item, 'before_update', Item.update_timestamp)
