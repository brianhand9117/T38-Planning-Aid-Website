"""
T-38 Planning Aid Email Service Flask Application
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from apscheduler.schedulers.background import BackgroundScheduler
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize extensions
db = SQLAlchemy()
mail = Mail()
scheduler = BackgroundScheduler()


def create_app(config_name='development', enable_scheduler=False):
    """
    Create and configure the Flask application
    
    Args:
        config_name: Configuration mode ('development' or 'production')
        enable_scheduler: If True, schedule background tasks (for worker mode)
                         If False, skip scheduling (for web server mode)
    """
    app = Flask(__name__)
    
    # Secret key for sessions/flash
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Configuration
    if config_name == 'development':
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
            'SQLALCHEMY_DATABASE_URI',
            'sqlite:///t38_email.db'
        )
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['DEBUG'] = True
    elif config_name == 'production':
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['DEBUG'] = False
    
    # Email Configuration
    smtp_testing = os.getenv('SMTP_TESTING', 'False').lower() == 'true'
    if smtp_testing:
        # Testing mode - print emails to console instead of sending
        app.config['MAIL_SUPPRESS_SEND'] = True
        app.config['TESTING'] = True
    
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 465))
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'False').lower() == 'true'
    app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL', 'True').lower() == 'true'
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')
    
    # Initialize extensions with app
    db.init_app(app)
    mail.init_app(app)
    
    # Register blueprints
    from app.routes import main_bp, admin_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    # Register scheduled tasks only if explicitly enabled
    # In production, the worker service handles scheduling
    if enable_scheduler:
        from app.tasks import schedule_kml_generation
        schedule_kml_generation(app)
    
    return app
