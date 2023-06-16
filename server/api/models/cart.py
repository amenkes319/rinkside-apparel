from sqlalchemy import func
from api import db
from api.models.user import User
from api.models.cart_item import CartItem

class Cart(db.Model):
    __tablename__ = 'carts'

    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    created_at = db.Column(db.TIMESTAMP, nullable=False, default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, nullable=False, default=db.func.current_timestamp())

    user = db.relationship('User', backref=db.backref('cart', uselist=False))
    items = db.relationship('CartItem', backref='cart', lazy=True)

    def __init__(self, id: int):
        self.id = id

    def __repr__(self):
        return f"Cart(id={self.id})"
    
    @staticmethod
    def update_timestamp(mapper, connection, target):
        target.updated_at = func.current_timestamp()
    
    def serialize(self):
        # return serialized cart with id and items
        return {
            'id': self.id,
            'items': [item.serialize() for item in self.items]
        }