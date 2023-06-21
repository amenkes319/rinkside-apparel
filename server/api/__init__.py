from flask_sqlalchemy import SQLAlchemy
from config import ApplicationConfig
from flask_session import Session
from .app_instance import app

db = SQLAlchemy()

def create_app():
    app.config.from_object(ApplicationConfig)
    server_session = Session(app)
    db.init_app(app)

    from .routes import api_bp
    app.register_blueprint(api_bp)

    return app
