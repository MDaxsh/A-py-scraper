from flask import Flask
from flask_cors import CORS
import os

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL',
        'postgresql://postgres:postgres@db:5432/myapp'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Enable CORS
    CORS(app)
    
    # Register blueprints
    from app.routes import api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')
    
    return app
