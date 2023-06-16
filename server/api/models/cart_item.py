from sqlalchemy import func
from api import db

class CartItem(db.Model):
    __tablename__ = 'cart_items'

    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    cart_id = db.Column(db.Integer, db.ForeignKey('carts.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    created_at = db.Column(db.TIMESTAMP, nullable=False, default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, nullable=False, default=db.func.current_timestamp())

    item = db.relationship('Item', backref='cart_items', lazy=True)

    def __init__(self, cart_id: int, item_id: int, quantity: int):
        self.cart_id = cart_id
        self.item_id = item_id
        self.quantity = quantity

    def __repr__(self):
        return f"CartItem(id={self.id}, item_id={self.item_id}, cart_id={self.cart_id}, quantity={self.quantity})"
    
    @staticmethod
    def update_timestamp(mapper, connection, target):
        target.updated_at = func.current_timestamp()

    def serialize(self):
        return {
            'id': self.id,
            'item_id': self.item_id,
            'cart_id': self.cart_id,
            'quantity': self.quantity
        }
