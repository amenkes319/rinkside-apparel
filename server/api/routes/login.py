from flask import Blueprint, request
from ..models import User

bp = Blueprint('login', __name__, url_prefix='/')

@bp.route('/', methods=['GET'])
def register():
    return 'Hello World!'

@bp.route('/login', methods=['GET'])
def login():
    users = User.query.all()
    return users[0].username
