from flask_sqlalchemy import SQLAlchemy
from app_instance import app
from config import ApplicationConfig

db = SQLAlchemy()

def create_app():
    app.config.from_object(ApplicationConfig)
    db.init_app(app)

    from .routes import api_bp
    app.register_blueprint(api_bp)

    return app
