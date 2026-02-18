"""
Background tasks for T-38 Planning Aid Email Service
"""
import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime
from flask import current_app
from flask_mail import Message
from app import db, mail, scheduler
from app.models import Subscriber, EmailLog, KMLGeneration


def generate_kml_file():
    """
    Run the T-38 Planning Aid GUI script to generate KML file
    Integrates with the existing GUI Files directory
    """
    try:
        repo_path = Path(os.getenv('KML_REPO_PATH', '../'))
        gui_script = repo_path / 'GUI Files' / 'T38_PlanAid_GUI.py'
        
        if not gui_script.exists():
            raise FileNotFoundError(f"GUI script not found at {gui_script}")
        
        # Run the GUI script (it will generate KML in KML_Output folder)
        # This assumes the script can run headless or we need to modify it
        result = subprocess.run(
            [sys.executable, str(gui_script)],
            capture_output=True,
            timeout=300,  # 5 minute timeout
            cwd=str(repo_path / 'GUI Files')
        )
        
        if result.returncode != 0:
            raise RuntimeError(f"KML generation failed: {result.stderr.decode()}")
        
        # Find the most recent KML file
        kml_output_dir = repo_path / 'KML_Output'
        kml_files = sorted(kml_output_dir.glob('*.kml'), key=lambda f: f.stat().st_mtime, reverse=True)
        
        if not kml_files:
            raise FileNotFoundError("No KML files found after generation")
        
        latest_kml = kml_files[0]
        
        # Record in database
        kml_gen = KMLGeneration(
            filename=latest_kml.name,
            filepath=str(latest_kml),
            file_size_mb=latest_kml.stat().st_size / (1024 * 1024),
            status='success'
        )
        db.session.add(kml_gen)
        db.session.commit()
        
        return kml_gen, latest_kml
        
    except Exception as e:
        current_app.logger.error(f"KML generation failed: {str(e)}")
        kml_gen = KMLGeneration(status='failed', error_message=str(e))
        db.session.add(kml_gen)
        db.session.commit()
        raise


def send_kml_emails(kml_gen, kml_path):
    """
    Send KML file to all active subscribers
    """
    try:
        subscribers = Subscriber.query.filter_by(is_active=True, is_verified=True).all()
        
        if not subscribers:
            current_app.logger.warning("No active subscribers found for KML email")
            return
        
        emails_sent = 0
        emails_failed = 0
        
        for subscriber in subscribers:
            try:
                msg = Message(
                    subject=f'T-38 Planning Aid - Latest Airport Data ({datetime.now().strftime("%B %Y")})',
                    recipients=[subscriber.email],
                    html=render_email_template(subscriber.first_name, kml_gen),
                    attachments=[(kml_gen.filename, open(kml_path, 'rb').read(), 'text/xml')]
                )
                
                mail.send(msg)
                
                # Log successful email
                email_log = EmailLog(
                    subscriber_id=subscriber.id,
                    subject=msg.subject,
                    kml_filename=kml_gen.filename,
                    kml_size_mb=kml_gen.file_size_mb,
                    status='sent'
                )
                db.session.add(email_log)
                emails_sent += 1
                
            except Exception as e:
                current_app.logger.error(f"Failed to send email to {subscriber.email}: {str(e)}")
                
                # Log failed email
                email_log = EmailLog(
                    subscriber_id=subscriber.id,
                    subject=f'T-38 Planning Aid - Latest Airport Data ({datetime.now().strftime("%B %Y")})',
                    kml_filename=kml_gen.filename,
                    status='failed',
                    error_message=str(e)
                )
                db.session.add(email_log)
                emails_failed += 1
        
        # Update KML generation record
        kml_gen.emails_sent = emails_sent
        kml_gen.emails_failed = emails_failed
        db.session.commit()
        
        current_app.logger.info(f"KML emails sent: {emails_sent}, failed: {emails_failed}")
        
    except Exception as e:
        current_app.logger.error(f"Error in email sending process: {str(e)}")
        raise


def render_email_template(subscriber_name, kml_gen):
    """
    Render the HTML email template for KML distribution
    """
    name_part = f"Hello {subscriber_name}," if subscriber_name else "Hello,"
    
    html = f"""
    <html>
        <body style="font-family: Arial, sans-serif; background-color: #0B3D91; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <!-- NASA-style header -->
                <div style="background: linear-gradient(135deg, #0B3D91 0%, #1B4EC5 100%); padding: 20px; text-align: center; border-radius: 8px 8px 0 0; margin: -20px -20px 20px -20px;">
                    <h1 style="color: white; margin: 0; font-size: 28px;">🚀 T-38 Planning Aid</h1>
                    <p style="color: #B0C4DE; margin: 5px 0 0 0; font-size: 14px;">Monthly Airport Data Update</p>
                </div>
                
                <p style="font-size: 16px; line-height: 1.6;">
                    {name_part}
                </p>
                
                <p style="font-size: 14px; line-height: 1.6; color: #555;">
                    Your monthly T-38 Planning Aid airport data file is ready! The attached KML file contains the latest 
                    airport information for ForeFlight and Google Earth, including:
                </p>
                
                <ul style="font-size: 14px; color: #555; line-height: 1.8;">
                    <li>T-38 eligible airports with up-to-date runway data</li>
                    <li>Government contract fuel availability</li>
                    <li>JASU (Air Start Cart) locations</li>
                    <li>Community feedback and comments</li>
                    <li>Color-coded airport pins for quick identification</li>
                </ul>
                
                <div style="background-color: #F0F8FF; border-left: 4px solid #0B3D91; padding: 15px; margin: 20px 0; border-radius: 4px;">
                    <p style="margin: 0; font-size: 13px; color: #555;">
                        <strong>File Details:</strong><br/>
                        File: {kml_gen.filename}<br/>
                        Generated: {kml_gen.generation_date.strftime('%B %d, %Y at %I:%M %p UTC')}<br/>
                        {f'Airports: {kml_gen.num_airports}' if kml_gen.num_airports else ''}
                    </p>
                </div>
                
                <p style="font-size: 14px; color: #555; line-height: 1.6;">
                    <strong>How to Use:</strong><br/>
                    1. Download the attached .kml file<br/>
                    2. Open it in ForeFlight, Google Earth, or your preferred flight planning tool<br/>
                    3. Use the color-coded pins to identify airport categories
                </p>
                
                <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
                
                <p style="font-size: 12px; color: #888; margin-bottom: 10px;">
                    <strong>Questions or Feedback?</strong><br/>
                    Contact your T-38 representative or fill out the feedback form at our website.
                </p>
                
                <div style="background-color: #f5f5f5; padding: 15px; text-align: center; border-radius: 4px;">
                    <p style="margin: 0; font-size: 12px; color: #666;">
                        © 2026 T-38 Planning Aid | Powered by NASA, USAF, and Community Flying
                    </p>
                </div>
            </div>
        </body>
    </html>
    """
    
    return html


def monthly_kml_job():
    """
    Scheduled job that runs monthly to generate KML and send emails
    """
    with current_app.app_context():
        current_app.logger.info("Starting monthly KML generation and email distribution")
        
        try:
            # Generate KML file
            kml_gen, kml_path = generate_kml_file()
            current_app.logger.info(f"KML generated successfully: {kml_gen.filename}")
            
            # Send emails to subscribers
            send_kml_emails(kml_gen, kml_path)
            current_app.logger.info("Monthly KML distribution completed")
            
        except Exception as e:
            current_app.logger.error(f"Monthly KML job failed: {str(e)}")


def schedule_kml_generation(app):
    """
    Schedule the monthly KML generation job
    """
    scheduler.add_job(
        monthly_kml_job,
        'cron',
        day=int(os.getenv('KML_SCHEDULE_DAY', 1)),
        hour=int(os.getenv('KML_SCHEDULE_HOUR', 9)),
        minute=int(os.getenv('KML_SCHEDULE_MINUTE', 0)),
        id='monthly_kml_generation',
        name='Monthly KML Generation and Email Distribution',
        replace_existing=True
    )
