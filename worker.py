"""
Worker process for T-38 Planning Aid Email Service
Runs APScheduler independently from Flask web server for autonomous operations
"""
import os
import sys
import time
import signal
import logging
from datetime import datetime
from app import create_app, db, scheduler
from app.tasks import schedule_kml_generation

# Ensure logs directory exists
os.makedirs('logs', exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('logs/worker.log')
    ]
)
logger = logging.getLogger('worker')

# Graceful shutdown flag
shutdown_requested = False


def signal_handler(signum, frame):
    """Handle shutdown signals gracefully"""
    global shutdown_requested
    logger.info(f"Received signal {signum}. Shutting down gracefully...")
    shutdown_requested = True
    if scheduler.running:
        scheduler.shutdown(wait=True)
    sys.exit(0)


def main():
    """Main worker process"""
    logger.info("="*60)
    logger.info("T-38 Planning Aid Worker Process Starting")
    logger.info(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("="*60)
    
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Create Flask app context for database access
    app = create_app(os.getenv('FLASK_ENV', 'production'))
    
    with app.app_context():
        # Ensure database tables exist
        try:
            db.create_all()
            logger.info("Database tables initialized")
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            sys.exit(1)
        
        # Schedule the KML generation job
        try:
            schedule_kml_generation(app)
            logger.info("KML generation job scheduled successfully")
        except Exception as e:
            logger.error(f"Failed to schedule KML generation job: {e}")
            sys.exit(1)
        
        # Start the scheduler
        if not scheduler.running:
            try:
                scheduler.start()
                logger.info("APScheduler started successfully")
                logger.info(f"Scheduler timezone: {scheduler.timezone}")
                
                # Log all scheduled jobs
                jobs = scheduler.get_jobs()
                logger.info(f"Scheduled jobs: {len(jobs)}")
                for job in jobs:
                    logger.info(f"  - Job: {job.name} (ID: {job.id})")
                    logger.info(f"    Next run: {job.next_run_time}")
                
            except Exception as e:
                logger.error(f"Failed to start scheduler: {e}")
                sys.exit(1)
        
        # Keep the process running
        logger.info("Worker process running. Press Ctrl+C to stop.")
        logger.info("-"*60)
        
        # Create heartbeat file for health checks
        heartbeat_file = '/tmp/worker_heartbeat'
        
        try:
            while not shutdown_requested:
                # Update heartbeat file
                with open(heartbeat_file, 'w') as f:
                    f.write(str(time.time()))
                
                # Sleep in small intervals to allow signal handling
                time.sleep(5)
                
        except KeyboardInterrupt:
            logger.info("Keyboard interrupt received")
        finally:
            logger.info("Shutting down worker process...")
            if scheduler.running:
                scheduler.shutdown(wait=True)
            # Clean up heartbeat file
            if os.path.exists(heartbeat_file):
                os.remove(heartbeat_file)
            logger.info("Worker process stopped")


if __name__ == '__main__':
    main()
