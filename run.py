"""
Main entry point for the T-38 Planning Aid Email Service website
For development use only - production uses gunicorn
"""
import os
from app import create_app, db, scheduler

# Determine if we should enable scheduler
# In development mode (when running this script directly), enable it
# In production (when using gunicorn), scheduler runs in worker service
enable_scheduler_in_dev = os.getenv('ENABLE_SCHEDULER_IN_DEV', 'True').lower() == 'true'

# Create Flask app
# In development mode with this script, we enable the scheduler unless explicitly disabled
# In production with gunicorn, create_app() is called without parameters (no scheduler)
if __name__ == '__main__':
    app = create_app(os.getenv('FLASK_ENV', 'development'), enable_scheduler=enable_scheduler_in_dev)
    
    with app.app_context():
        # Create database tables
        db.create_all()
        
        # Start the scheduler if enabled and not already running
        if enable_scheduler_in_dev and not scheduler.running:
            scheduler.start()
            print("✅ Scheduler started in development mode")
    
    # Run the Flask app
    app.run(
        host=os.getenv('FLASK_HOST', '0.0.0.0'),
        port=int(os.getenv('FLASK_PORT', 5000)),
        debug=os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    )
else:
    # When imported by gunicorn or other WSGI servers
    # Don't enable scheduler - it runs in worker service
    app = create_app(os.getenv('FLASK_ENV', 'production'), enable_scheduler=False)
