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
    
    # Sample projects data
    projects = [
        {
            'id': 1,
            'title': 'Project One',
            'description': 'A amazing web application built with modern technologies',
            'technologies': ['Python', 'Flask', 'HTML', 'CSS', 'JavaScript'],
            'image': 'project1.jpg',
            'live_url': '#',
            'github_url': '#'
        },
        {
            'id': 2,
            'title': 'Project Two',
            'description': 'An innovative solution for real-world problems',
            'technologies': ['React', 'Node.js', 'MongoDB'],
            'image': 'project2.jpg',
            'live_url': '#',
            'github_url': '#'
        },
        {
            'id': 3,
            'title': 'Project Three',
            'description': 'A data analysis dashboard with interactive visualizations',
            'technologies': ['Python', 'Pandas', 'D3.js', 'Flask'],
            'image': 'project3.jpg',
            'live_url': '#',
            'github_url': '#'
        }
    ]
    
    # Sample skills data
    skills = [
        {'name': 'Python', 'level': 90, 'category': 'Programming'},
        {'name': 'JavaScript', 'level': 85, 'category': 'Programming'},
        {'name': 'HTML/CSS', 'level': 90, 'category': 'Web Development'},
        {'name': 'Flask', 'level': 85, 'category': 'Web Development'},
        {'name': 'React', 'level': 75, 'category': 'Web Development'},
        {'name': 'Git', 'level': 80, 'category': 'Tools'},
        {'name': 'SQL', 'level': 70, 'category': 'Database'},
        {'name': 'MongoDB', 'level': 65, 'category': 'Database'}
    ]
    
    # Make data available to all templates
    app.jinja_env.globals['config'] = portfolio_config
    app.jinja_env.globals['projects'] = projects
    app.jinja_env.globals['skills'] = skills
    
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
