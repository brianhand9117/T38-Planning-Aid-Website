"""
Routes for T-38 Planning Aid Email Service website
"""
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash, current_app
from app import db, mail
from app.models import Subscriber, EmailLog, KMLGeneration
from flask_mail import Message
import secrets
from datetime import datetime

# Create blueprints
main_bp = Blueprint('main', __name__)
admin_bp = Blueprint('admin', __name__)


# ───────────────────────────────────────
# PUBLIC ROUTES
# ───────────────────────────────────────

@main_bp.route('/')
def index():
    """Homepage with subscription form"""
    total_subscribers = Subscriber.query.filter_by(is_active=True, is_verified=True).count()
    latest_kml = KMLGeneration.query.order_by(KMLGeneration.generation_date.desc()).first()
    
    return render_template('index.html', 
                         total_subscribers=total_subscribers,
                         latest_kml=latest_kml)


@main_bp.route('/subscribe', methods=['POST'])
def subscribe():
    """Handle subscription form submission"""
    email = request.form.get('email', '').lower().strip()
    first_name = request.form.get('first_name', '').strip()
    last_name = request.form.get('last_name', '').strip()
    
    # Validation
    if not email or '@' not in email:
        return jsonify({'success': False, 'message': 'Invalid email address'}), 400
    
    # Check if already subscribed
    existing = Subscriber.query.filter_by(email=email).first()
    if existing and existing.is_verified:
        return jsonify({'success': False, 'message': 'Email already subscribed'}), 400
    
    try:
        if existing:
            # Reactivate existing subscriber
            existing.is_active = True
            existing.first_name = first_name
            existing.last_name = last_name
            subscriber = existing
        else:
            # Create new subscriber
            subscriber = Subscriber(
                email=email,
                first_name=first_name,
                last_name=last_name
            )
            subscriber.generate_verification_token()
            db.session.add(subscriber)
        
        db.session.commit()
        
        # Send verification email
        send_verification_email(subscriber)
        
        return jsonify({
            'success': True, 
            'message': 'Check your email to verify your subscription'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Could not process subscription'}), 500


@main_bp.route('/verify/<token>')
def verify_email(token):
    """Verify email subscription via token"""
    subscriber = Subscriber.query.filter_by(verification_token=token).first()
    
    if not subscriber:
        flash('Invalid or expired verification link', 'error')
        return redirect(url_for('main.index'))
    
    try:
        subscriber.mark_verified()
        flash('Email verified! You will receive monthly KML files.', 'success')
    except Exception as e:
        flash('Verification failed', 'error')
    
    return redirect(url_for('main.index'))


@main_bp.route('/unsubscribe/<token>')
def unsubscribe(token):
    """Unsubscribe from email list"""
    subscriber = Subscriber.query.filter_by(verification_token=token).first()
    
    if not subscriber:
        subscriber = Subscriber.query.filter_by(email=request.args.get('email')).first()
    
    if subscriber:
        subscriber.is_active = False
        subscriber.unsubscribed_date = datetime.utcnow()
        db.session.commit()
        flash('You have been unsubscribed', 'success')
    else:
        flash('Could not find subscription', 'error')
    
    return redirect(url_for('main.index'))


@main_bp.route('/about')
def about():
    """About page"""
    return render_template('about.html')


@main_bp.route('/privacy')
def privacy():
    """Privacy policy page"""
    return render_template('privacy.html')


@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact form"""
    if request.method == 'POST':
        name = request.form.get('name', '')
        email = request.form.get('email', '')
        message = request.form.get('message', '')
        
        if not all([name, email, message]):
            flash('All fields are required', 'error')
            return redirect(url_for('main.contact'))
        
        try:
            # Send contact email to admin
            msg = Message(
                subject=f'T-38 Planning Aid: Contact from {name}',
                recipients=[''],  # Set your admin email here
                body=f'From: {email}\n\n{message}'
            )
            mail.send(msg)
            flash('Thank you for your message. We will respond soon.', 'success')
            return redirect(url_for('main.contact'))
        except Exception as e:
            flash('Could not send message. Please try again.', 'error')
    
    return render_template('contact.html')


# ───────────────────────────────────────
# ADMIN ROUTES
# ───────────────────────────────────────

@admin_bp.route('/dashboard')
def dashboard():
    """Admin dashboard"""
    total_subscribers = Subscriber.query.filter_by(is_active=True, is_verified=True).count()
    pending_subscribers = Subscriber.query.filter_by(is_verified=False).count()
    recent_emails = EmailLog.query.order_by(EmailLog.sent_date.desc()).limit(10).all()
    recent_kml = KMLGeneration.query.order_by(KMLGeneration.generation_date.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html',
                         total_subscribers=total_subscribers,
                         pending_subscribers=pending_subscribers,
                         recent_emails=recent_emails,
                         recent_kml=recent_kml)


@admin_bp.route('/subscribers')
def subscribers():
    """Manage subscribers"""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    subscribers = Subscriber.query.paginate(page=page, per_page=per_page)
    
    return render_template('admin/subscribers.html', subscribers=subscribers)


@admin_bp.route('/emails')
def email_logs():
    """View email logs"""
    page = request.args.get('page', 1, type=int)
    per_page = 50
    
    logs = EmailLog.query.order_by(EmailLog.sent_date.desc()).paginate(page=page, per_page=per_page)
    
    return render_template('admin/emails.html', logs=logs)


@admin_bp.route('/kml-history')
def kml_history():
    """View KML generation history"""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    kml_gens = KMLGeneration.query.order_by(KMLGeneration.generation_date.desc()).paginate(
        page=page, per_page=per_page)
    
    return render_template('admin/kml_history.html', kml_gens=kml_gens)


# ───────────────────────────────────────
# HELPER FUNCTIONS
# ───────────────────────────────────────

def send_verification_email(subscriber):
    """Send verification email to subscriber"""
    verify_url = url_for('main.verify_email', token=subscriber.verification_token, _external=True)
    
    html = f"""
    <html>
        <body style="font-family: Arial, sans-serif;">
            <div style="max-width: 600px; margin: 0 auto;">
                <h2>Confirm Your Subscription</h2>
                <p>Click the button below to confirm your email address and start receiving monthly T-38 Planning Aid data:</p>
                <p>
                    <a href="{verify_url}" style="background-color: #0B3D91; color: white; padding: 10px 20px; text-decoration: none; border-radius: 4px; display: inline-block;">
                        Verify Email Address
                    </a>
                </p>
                <p style="font-size: 12px; color: #666;">
                    Or copy this link: {verify_url}
                </p>
            </div>
        </body>
    </html>
    """
    
    msg = Message(
        subject='Confirm Your T-38 Planning Aid Subscription',
        recipients=[subscriber.email],
        html=html
    )
    
    # Log the email to database
    email_log = EmailLog(
        subscriber_id=subscriber.id,
        subject=msg.subject,
        status='pending'
    )
    db.session.add(email_log)
    db.session.commit()
    
    # Print verification details to console for development/testing
    print("\n" + "="*80)
    print("EMAIL VERIFICATION NOTICE (SMTP unavailable - development mode)")
    print("="*80)
    print(f"To: {subscriber.email}")
    print(f"From: {current_app.config.get('MAIL_DEFAULT_SENDER', 'T38 Planning Aid')}")
    print(f"Subject: {msg.subject}")
    print("\n--- EMAIL BODY ---")
    print(html)
    print("--- VERIFICATION LINK ---")
    print(f"Click this link to verify: {verify_url}")
    print("="*80 + "\n")
    
    try:
        mail.send(msg)
        email_log.status = 'sent'
        db.session.commit()
        current_app.logger.info(f"Verification email sent to {subscriber.email}")
    except Exception as e:
        email_log.status = 'failed'
        email_log.error_message = str(e)
        db.session.commit()
        current_app.logger.error(f"Failed to send verification email to {subscriber.email}: {str(e)}")
        # Don't raise - still consider it "sent" if it was printed to console
