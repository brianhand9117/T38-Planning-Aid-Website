#!/usr/bin/env python
"""Test email verification flow"""

import requests

BASE_URL = 'http://localhost:5000'

# Get the token from the latest subscription (we know it from the app output)
token = '6da9ba441fc7ed23dc92f0fe0c7b79a9859e23ceccdd6041f76762dfff8fd281'

print("Testing email verification...")
print("=" * 60)
print(f"\nGET {BASE_URL}/verify/{token}")

response = requests.get(f'{BASE_URL}/verify/{token}', allow_redirects=False)

print(f"\nStatus Code: {response.status_code}")
print(f"Location Header: {response.headers.get('Location', 'None')}")

if response.status_code in (301, 302):
    print(f"\n✓ Verification successful! Redirected to {response.headers['Location']}")
else:
    print(f"Response: {response.text[:200]}")

print("\n" + "=" * 60)
print("Subscriber should now be verified in database")
