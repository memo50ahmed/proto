from flask import Flask
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv('SECRET_KEY', 'default-secret-key')
    
    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize database
    from .models import db
    db.init_app(app)
    
    # Portfolio data from environment
    portfolio_config = {
        'name': os.getenv('PORTFOLIO_NAME', ''),
        'email': os.getenv('PORTFOLIO_EMAIL', ''),
        'title': os.getenv('PORTFOLIO_TITLE', 'Portfolio | ' + os.getenv('PORTFOLIO_NAME', '')),
        'description': os.getenv('PORTFOLIO_DESCRIPTION', ''),
        'github': os.getenv('GITHUB_URL', '#'),
        'linkedin': os.getenv('LINKEDIN_URL', '#'),
        'facebook': os.getenv('FACEBOOK_URL', '#')
    }
    
    # Make data available to all templates
    app.jinja_env.globals['config'] = portfolio_config
    
    # Import and register routes
    from . import routes
    app.register_blueprint(routes.main_bp)
    
    # Import and register admin routes
    from . import admin
    app.register_blueprint(admin.admin_bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app
