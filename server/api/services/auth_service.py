from sqlalchemy import func
from ..models.user import User
from .. import db

def register_user(username, password):
    if not username or not password:
        return {"error": "Username or Password missing"}, 400

    user = User.query.filter_by(username=username).first()

    if user:
        return {"error": "Username already exists"}, 400

    max_id = db.session.query(func.max(User.id)).scalar()
    new_id = int(max_id) + 1 if max_id else 1

    new_user = User(id=new_id, username=username, password=password)

    db.session.add(new_user)
    db.session.commit()

    return {"message": "User created successfully!"}, 201

def login_user(username, password):
    if not username or not password:
        return {"error": "Username or Password missing"}, 400

    user = User.query.filter_by(username=username).first()

    if not user or not user.check_password(password):
        return {"error": "Invalid username or password"}, 401

    return {"message": "Logged in successfully!"}, 200
