from flask import Blueprint, request
from ..models import User
from ..services.auth_service import register_user, login_user

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['POST'])
def register():
    return register_user(request.json.get('username'), request.json.get('password'))

@bp.route('/login', methods=['POST'])
def login():
    return login_user(request.json.get('username'), request.json.get('password'))
