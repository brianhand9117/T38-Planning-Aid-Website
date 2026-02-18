"""
Main entry point for the T-38 Planning Aid Email Service website
"""
import os
from app import create_app, db, scheduler

# Create Flask app
app = create_app(os.getenv('FLASK_ENV', 'development'))

if __name__ == '__main__':
    with app.app_context():
        # Create database tables
        db.create_all()
        
        # Start the scheduler for monthly KML generation and emails
        if not scheduler.running:
            scheduler.start()
    
    # Run the Flask app
    app.run(
        host=os.getenv('FLASK_HOST', '0.0.0.0'),
        port=int(os.getenv('FLASK_PORT', 5000)),
        debug=os.getenv('FLASK_DEBUG', True)
    )
