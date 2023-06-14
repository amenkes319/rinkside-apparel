from flask import Blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api')

from .user_routes import bp as user_bp
api_bp.register_blueprint(user_bp)

from .item_routes import bp as item_bp
api_bp.register_blueprint(item_bp)
