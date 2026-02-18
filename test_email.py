#!/usr/bin/env python
"""Test email configuration"""

from app import create_app, mail, db
from app.models import Subscriber
from flask_mail import Message
from dotenv import load_dotenv

load_dotenv()

app = create_app()

with app.app_context():
    # Check config
    print('Email Configuration:')
    print(f'  SMTP Server: {app.config["MAIL_SERVER"]}')
    print(f'  SMTP Port: {app.config["MAIL_PORT"]}')
    print(f'  TLS: {app.config["MAIL_USE_TLS"]}')
    print(f'  Username: {app.config["MAIL_USERNAME"]}')
    print(f'  Default Sender: {app.config["MAIL_DEFAULT_SENDER"]}')
    print()
    
    # Get subscriber
    subscriber = Subscriber.query.filter_by(email='brianhand54@gmail.com').first()
    if subscriber:
        print(f'Subscriber found:')
        print(f'  Email: {subscriber.email}')
        print(f'  Verified: {subscriber.is_verified}')
        print(f'  Active: {subscriber.is_active}')
        print(f'  Verification Token: {subscriber.verification_token}')
        print()
        
        # Test send verification email
        try:
            verify_url = f'http://localhost:5000/verify/{subscriber.verification_token}'
            
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
            mail.send(msg)
            print('SUCCESS: Verification email sent!')
            print(f'Verify link: {verify_url}')
        except Exception as e:
            print(f'ERROR sending verification email: {str(e)}')
            import traceback
            traceback.print_exc()
    else:
        print('No subscriber found with email brianhand54@gmail.com')
