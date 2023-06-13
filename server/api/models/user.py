from werkzeug.security import generate_password_hash, check_password_hash
from api import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.current_timestamp(), server_onupdate=db.func.current_timestamp())

    def __init__(self, id: int, username: str, password: str):
        self.id = id
        self.username = username
        self.set_password(password)

    def __str__(self):
        return f'User[id={self.id}, username={self.username}]'

    @staticmethod
    def update_timestamp(mapper, connection, target):
        target.updated_at = db.func.current_timestamp()

    def set_password(self, password: str):
        self.password = generate_password_hash(password, method='scrypt', salt_length=16)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)
    
    def serialize(self) -> dict:
        return {
            'id': self.id,
            'username': self.username
        }
