from flask import Blueprint, Response, jsonify, make_response, request 
from api.services import user_service
from api.models.user import User

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/login/', methods=['POST'])
def login() -> Response:
    """
    Response to a POST request to /user/login. Logs a user in.

    :param username: The username of the user to log in.
    :param password: The password of the user to log in.

    :return: Response with HTTP status of BAD_REQUEST if the username or password is missing.
    Response with HTTP status of UNAUTHORIZED if the username or password is incorrect.
    Response with HTTP status of OK and the user.
    """
    data = request.authorization
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return make_response(jsonify({"error": "Username or Password missing"}), 400)

    user = user_service.login(username, password)
    if user:
        return make_response(jsonify(user.serialize()), 200)
    return make_response(jsonify({"error": "Username or Password incorrect"}), 401)

@bp.route('/', methods=['GET'])
def get_users() -> Response:
    """
    Response to a GET request to /user. Gets all users from the database.

    :return: Response with HTTP status of OK and a list of users.
    """
    users = user_service.get_users()
    return make_response(jsonify([user.serialize() for user in users]), 200)

@bp.route('/', methods=['POST'])
def create_user() -> Response:
    """
    Response to a POST request to /user. Creates a new user and adds it to the database.

    :param user: A user object with the username and password of the new user.

    :return: Response with HTTP status of BAD_REQUEST if the username or password is missing.
    Response with HTTP status of CONFLICT if the username already exists.
    Response with HTTP status of CREATED if the user was created successfully.
    """
    auth = request.authorization
    username = auth.get('username')
    password = auth.get('password')
    if not username or not password:
        return make_response(jsonify({"error": "Username or Password missing"}), 400)

    user = user_service.register_user(username, password)
    if user:
        return make_response(jsonify(user.serialize()), 201)
    return make_response(jsonify({"error": "Username already exists"}), 409)

@bp.route('/<int:id>/', methods=['GET'])
def get_user(id: int) -> Response:
    """
    Response to a GET request to /user/<id>. Gets a user from the database.

    :param id: The id of the user to get.

    :return: Response with HTTP status of NOT_FOUND if the user does not exist.
    Response with HTTP status of OK and the user.
    """
    user = user_service.get_user(id)
    if not user:
        return make_response(jsonify({"error": "User not found"}), 404)
    return make_response(jsonify(user.serialize()), 200)

@bp.route('/<int:id>/', methods=['PUT'])
def update_user(id: int) -> Response:
    """
    Response to a PUT request to /user/<id>. Updates a user in the database.

    :param id: The id of the user to update.
    :param user: A user object with the updated information.

    :return: Response with HTTP status of BAD_REQUEST if the user data is invalid.
    Response with HTTP status of NOT_FOUND if the user does not exist.
    Response with HTTP status of CONFLICT if the username already exists.
    Response with HTTP status of OK if the user was updated successfully.
    """
    user_data = request.json
    try:
        new_user = User(id, **user_data)
        user, error = user_service.update_user(new_user)
        if user:
            return make_response(jsonify(user.serialize()), 200)
        
        if error == "User not found":
            error_code = 404
        elif error == "Username already exists":
            error_code = 409
        return make_response(jsonify({"error": error}), error_code)
    except TypeError:
        return make_response(jsonify({"error": "Invalid user data"}), 400)
    
@bp.route('/<int:id>/', methods=['DELETE'])
def delete_user(id: int) -> Response:
    """
    Response to a DELETE request to /user/<id>. Deletes a user from the database.
    
    :param id: The id of the user to delete.

    :return: Response with HTTP status of NOT_FOUND if the user does not exist.
    Response with HTTP status of OK if the user was deleted successfully.
    """
    delete_success = user_service.delete_user(id)
    if delete_success:
        return make_response(jsonify({"message": "User deleted"}), 200)
    return make_response(jsonify({"error": "User not found"}), 404)
