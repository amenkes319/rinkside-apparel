from .user import User
from sqlalchemy import event

event.listen(User, 'before_update', User.update_timestamp)
