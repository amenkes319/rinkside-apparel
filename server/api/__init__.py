import os
from flask_sqlalchemy import SQLAlchemy
from .app_instance import app

db = SQLAlchemy()

def create_app():
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    db.init_app(app)

    from .routes import api_bp
    app.register_blueprint(api_bp)

    return app
