from sqlalchemy import func
from api import db

class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    image_url = db.Column(db.String(1024))
    category = db.Column(db.String(255))
    size = db.Column(db.String(50))
    color = db.Column(db.String(50))
    stock = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.TIMESTAMP, nullable=False, default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, nullable=False, default=db.func.current_timestamp())

    def __init__(self, name, price, stock, description=None, image_url=None, category=None, size=None, color=None):
        self.name = name
        self.description = description
        self.price = price
        self.image_url = image_url
        self.category = category
        self.size = size
        self.color = color
        self.stock = stock

    @staticmethod
    def update_timestamp(mapper, connection, target):
        target.updated_at = func.current_timestamp()

    def serialize(self):
        return {
            'id': self.id, 
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'image_url': self.image_url,
            'category': self.category,
            'size': self.size,
            'color': self.color,
            'stock': self.stock
        }
    