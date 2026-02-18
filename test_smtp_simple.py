#!/usr/bin/env python
"""Simple SMTP test - direct smtplib test"""

import smtplib
import ssl

print("Testing SMTP connectivity...")

# Test port 587 with TLS
print("\n1. Testing smtp.gmail.com:587 with STARTLS (TLS)...")
try:
    server = smtplib.SMTP('smtp.gmail.com', 587, timeout=5)
    print("   ✓ Connected")
    server.starttls(context=ssl.create_default_context())
    print("   ✓ STARTLS successful")
    server.login('brianhand54@gmail.com', 'rbmcjglvlmtrvmgi')
    print("   ✓ Authentication successful")
    server.quit()
    print("   ✓ 587/TLS works!")
except Exception as e:
    print(f"   ✗ Error: {type(e).__name__}: {e}")

# Test port 465 with SSL
print("\n2. Testing smtp.gmail.com:465 with implicit SSL...")
try:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=5)
    print("   ✓ Connected")
    server.login('brianhand54@gmail.com', 'rbmcjglvlmtrvmgi')
    print("   ✓ Authentication successful")
    server.quit()
    print("   ✓ 465/SSL works!")
except Exception as e:
    print(f"   ✗ Error: {type(e).__name__}: {e}")

print("\nDone!")
