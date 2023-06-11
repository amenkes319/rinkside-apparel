from flask import Blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api')

from .login import bp as login_bp
api_bp.register_blueprint(login_bp)
