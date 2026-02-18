"""
Database models for T-38 Planning Aid Email Service
"""
from app import db
from datetime import datetime
import hashlib


class Subscriber(db.Model):
    """Email subscriber model"""
    __tablename__ = 'subscribers'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    verification_token = db.Column(db.String(255), unique=True)
    subscribed_date = db.Column(db.DateTime, default=datetime.utcnow)
    unsubscribed_date = db.Column(db.DateTime)
    notes = db.Column(db.Text)
    
    # Relationships
    email_logs = db.relationship('EmailLog', back_populates='subscriber', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Subscriber {self.email}>'
    
    def generate_verification_token(self):
        """Generate a unique verification token"""
        token_data = f"{self.email}{datetime.utcnow().isoformat()}".encode('utf-8')
        self.verification_token = hashlib.sha256(token_data).hexdigest()
        return self.verification_token
    
    def mark_verified(self):
        """Mark subscriber as verified"""
        self.is_verified = True
        self.verification_token = None
        db.session.commit()


class EmailLog(db.Model):
    """Log of sent emails for tracking"""
    __tablename__ = 'email_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    subscriber_id = db.Column(db.Integer, db.ForeignKey('subscribers.id'), nullable=False)
    subject = db.Column(db.String(255), nullable=False)
    sent_date = db.Column(db.DateTime, default=datetime.utcnow)
    kml_filename = db.Column(db.String(255))
    kml_size_mb = db.Column(db.Float)
    status = db.Column(db.String(50), default='sent')  # sent, bounced, failed
    error_message = db.Column(db.Text)
    
    # Relationships
    subscriber = db.relationship('Subscriber', back_populates='email_logs')
    
    def __repr__(self):
        return f'<EmailLog {self.subject} -> {self.subscriber.email}>'


class KMLGeneration(db.Model):
    """Track KML file generation history"""
    __tablename__ = 'kml_generations'
    
    id = db.Column(db.Integer, primary_key=True)
    generation_date = db.Column(db.DateTime, default=datetime.utcnow)
    filename = db.Column(db.String(255), nullable=False)
    filepath = db.Column(db.String(500), nullable=False)
    file_size_mb = db.Column(db.Float)
    num_airports = db.Column(db.Integer)
    status = db.Column(db.String(50), default='success')  # success, failed
    error_message = db.Column(db.Text)
    emails_sent = db.Column(db.Integer, default=0)
    emails_failed = db.Column(db.Integer, default=0)
    
    def __repr__(self):
        return f'<KMLGeneration {self.filename} on {self.generation_date}>'
