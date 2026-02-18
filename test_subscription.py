#!/usr/bin/env python
"""Test subscription flow"""

import requests
import json

BASE_URL = 'http://localhost:5000'

print("Testing subscription form...")
print("=" * 60)

# Test data (as form data, not JSON)
subscription_data = {
    'email': 'testuser@example.com',
    'first_name': 'Test',
    'last_name': 'User'
}

# POST to subscribe endpoint
print(f"\nPOST {BASE_URL}/subscribe")
print(f"Data: {json.dumps(subscription_data)}")

response = requests.post(
    f'{BASE_URL}/subscribe',
    data=subscription_data  # Use form data instead of JSON
)

print(f"\nStatus Code: {response.status_code}")
print(f"Response: {response.text}")

if response.status_code == 200:
    data = response.json()
    if data.get('success'):
        print("\n✓ Subscription successful!")
        print(f"Message: {data.get('message')}")
    else:
        print(f"\n✗ Subscription failed: {data.get('message')}")
else:
    print(f"\n✗ Error: HTTP {response.status_code}")

print("\n" + "=" * 60)
print("Check the Flask server terminal for email output")
