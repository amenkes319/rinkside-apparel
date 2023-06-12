from sqlalchemy import func
from api.models.user import User
from api import db

def get_users() -> list[User]:
    """
    Gets all users from the database.

    :return: A list of users.
    """
    return User.query.all()

def get_user(id) -> User:
    """
    Gets a user from the database.
    If the user does not exist, returns None.

    :param id: The id of the user to get.

    :return: A user.
    """
    return User.query.get(id)

def register_user(username: str, password: str) -> User:
    """
    Creates a new user and adds it to the database.

    :param username: The username of the new user.
    :param password: The password of the new user.
    :return: True if the user was created successfully, False if the username already exists.
    """
    user = User.query.filter_by(username=username).first()
    if user:
        return None

    # Get the max id from the database and increment it by 1 to get the new id
    max_id = db.session.query(func.max(User.id)).scalar()
    new_id = int(max_id) + 1 if max_id else 1

    new_user = User(id=new_id, username=username, password=password)

    db.session.add(new_user)
    db.session.commit()

    return new_user

def update_user(user: User) -> tuple[User, str]:
    """
    Updates the given user in the database.

    :param user: A user object with the updated information.

    :return: A tuple containing the updated user and an error message if the user does not exist or the username already exists.
    """
    user_to_update = User.query.get(user.id)
    if not user_to_update:
        return None, "User not found"
    
    if user.username != user_to_update.username:
        existing_user = User.query.filter_by(username=user.username).first()
        if existing_user:
            return None, "Username already exists"

    user_to_update.username = user.username
    if not user_to_update.password == user.password:
        user_to_update.password = user.password

    db.session.commit()

    return user_to_update, None

def delete_user(id: int) -> bool:
    """
    Deletes the given user from the database.
    
    :param id: The id of the user to delete.
    
    :return: True if the user was deleted successfully, False if the user does not exist.
    """
    user = User.query.get(id)
    if not user:
        return False
    
    db.session.delete(user)
    db.session.commit()

    return True

def login(username: str, password: str):
    """
    Attempts to log the user in.

    :param username: The username of the user to log in.
    :param password: The password of the user to log in.

    :return: The user if the username and password are correct, None if the username or password is incorrect.
    """
    user = User.query.filter_by(username=username).first()
    if not user:
        return None
    
    if not user.check_password(password):
        return None
    
    return user
