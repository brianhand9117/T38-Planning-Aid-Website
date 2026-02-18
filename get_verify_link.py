#!/usr/bin/env python
"""Get verification token for a specific email"""

from app import create_app, db
from app.models import Subscriber

app = create_app()

with app.app_context():
    subscriber = Subscriber.query.filter_by(email='brianhand54@gmail.com').first()
    
    if subscriber:
        print("\n" + "=" * 80)
        print("VERIFICATION LINK FOR brianhand54@gmail.com")
        print("=" * 80)
        print(f"\nEmail: {subscriber.email}")
        print(f"Name: {subscriber.first_name} {subscriber.last_name}")
        print(f"Verified: {subscriber.is_verified}")
        print(f"Active: {subscriber.is_active}")
        print(f"\nVerification Token:")
        print(f"  {subscriber.verification_token}")
        print(f"\nVerification Link:")
        print(f"  http://localhost:5000/verify/{subscriber.verification_token}")
        print(f"\nTo verify:")
        print(f"  1. Copy the link above")
        print(f"  2. Paste into your browser")
        print(f"  3. Or run: python -c \"import requests; requests.get('http://localhost:5000/verify/{subscriber.verification_token}')\"")
        print("=" * 80)
    else:
        print("Subscriber not found!")
