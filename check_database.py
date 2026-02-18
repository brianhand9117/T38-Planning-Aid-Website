#!/usr/bin/env python
"""Check subscriber status in database"""

from app import create_app, db
from app.models import Subscriber, EmailLog

app = create_app()

with app.app_context():
    # Check all subscribers
    subscribers = Subscriber.query.all()
    
    print("\n" + "=" * 80)
    print("SUBSCRIBERS IN DATABASE")
    print("=" * 80)
    
    for sub in subscribers:
        print(f"\nEmail: {sub.email}")
        print(f"  Name: {sub.first_name} {sub.last_name}")
        print(f"  Active: {sub.is_active}")
        print(f"  Verified: {sub.is_verified}")
        print(f"  Subscribed: {sub.subscribed_date}")
        if sub.verification_token:
            print(f"  Token: {sub.verification_token[:20]}...")
    
    print("\n" + "=" * 80)
    print("EMAIL LOGS")
    print("=" * 80)
    
    logs = EmailLog.query.all()
    print(f"Total emails logged: {len(logs)}")
    for log in logs:
        print(f"\n  To: {log.subscriber.email if log.subscriber else 'N/A'}")
        print(f"  Subject: {log.subject}")
        print(f"  Status: {log.status}")
        print(f"  Sent: {log.sent_date}")
