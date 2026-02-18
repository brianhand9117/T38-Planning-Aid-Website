"""
WSGI configuration for PythonAnywhere deployment
This file is required by PythonAnywhere to run the Flask application
"""
import os
import sys

# Add the website directory to the path so imports work
website_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, website_dir)

# Create the Flask app
from app import create_app, db, scheduler

app = create_app(os.getenv('FLASK_ENV', 'production'))

# Initialize database
with app.app_context():
    db.create_all()
    
    # Start scheduler if not already running
    if not scheduler.running:
        scheduler.start()
