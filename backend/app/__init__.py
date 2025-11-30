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
    from app.jobs_routes import jobs_blueprint
    from app.scraper_routes import scraper_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')
    app.register_blueprint(jobs_blueprint, url_prefix='/api/jobs')
    app.register_blueprint(scraper_blueprint, url_prefix='/api/scraper')
    
    return app
