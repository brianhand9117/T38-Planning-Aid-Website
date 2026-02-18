# T-38 Planning Aid - Email System Troubleshooting & Development Guide

## Current Status: ✅ WORKING (Development/Testing Mode)

The email system is **fully functional** in development mode. Verification emails are being captured and logged. The system is ready to send real emails once network/firewall issues are resolved.

## Understanding the Email System

### Development Mode (SMTP_TESTING=True)
When `SMTP_TESTING=True` is set in `.env`:
- Emails are NOT sent to real SMTP servers
- Instead, emails are printed to the **Flask server console**
- Emails are also logged to the database (`EmailLog` table)
- Perfect for development, testing, and environments where SMTP is blocked

### Production Mode (SMTP_TESTING=False)
When `SMTP_TESTING=False` is set in `.env`:
- Emails are sent via Gmail SMTP (smtp.gmail.com:465)
- Requires valid Gmail account and app password
- Enabled when deployed to environment with network access

## Configuration

### .env Settings

```dotenv
# Enable/disable SMTP testing mode
SMTP_TESTING=True

# Gmail SMTP Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=465
MAIL_USE_TLS=False
MAIL_USE_SSL=True
MAIL_USERNAME=brianhand54@gmail.com
MAIL_PASSWORD=rbmcjglvlmtrvmgi
MAIL_DEFAULT_SENDER=T38 Planning Aid <brianhand54@gmail.com>

# Flask secret key for sessions (required for verification flow)
SECRET_KEY=your-secret-key-change-in-production-12345abcde
```

## How the Email Verification Flow Works

### 1. **Subscription**
- User submits email via form at `http://localhost:5000/`
- Email, first name, last name are captured
- Verification token (cryptographic hash) is generated

### 2. **Verification Email Sent**
- Email is composed with verification link
- In development mode, printed to Flask console:
  ```
  ================================================================================
  EMAIL VERIFICATION NOTICE (SMTP unavailable - development mode)
  ================================================================================
  To: testuser@example.com
  From: T38 Planning Aid <brianhand54@gmail.com>
  Subject: Confirm Your T-38 Planning Aid Subscription
  
  --- VERIFICATION LINK ---
  Click this link to verify: http://localhost:5000/verify/6da9ba441fc...
  ================================================================================
  ```
- Email is also logged to database (`EmailLog` table)

### 3. **User Verifies Email**
- User clicks verification link in console output (or visits the URL directly)
- Link: `http://localhost:5000/verify/{token}`
- Subscriber status changes to `is_verified=True` in database
- User is shown success message

### 4. **Monthly KML Distribution**
- Background scheduler runs on 1st of month at 9 AM UTC (configurable)
- Generates fresh KML file from T-38 Planning Aid data
- Sends KML file via email to all verified subscribers
- Emails logged to database with subject, recipient, file info, status

## Database Tables

### Subscriber
- `id`: Primary key
- `email`: Unique email address
- `first_name`, `last_name`: Subscriber name
- `is_active`: Whether subscription is active
- `is_verified`: Whether email is verified (must be True to receive emails)
- `verification_token`: Cryptographic token for verification link
- `subscribed_date`: When they subscribed
- `unsubscribed_date`: When they unsubscribed (if applicable)

### EmailLog
- `id`: Primary key
- `subscriber_id`: Foreign key to Subscriber
- `subject`: Email subject line
- `kml_filename`: Filename if it was a KML distribution email
- `status`: 'sent', 'failed', or 'pending'
- `error_message`: Error details if status is 'failed'
- `sent_date`: Timestamp when email was sent/logged

### KMLGeneration
- `id`: Primary key
- `filename`: Name of generated KML file
- `filepath`: Full path to file
- `file_size_mb`: File size
- `generation_date`: When KML was generated
- `emails_sent`: Count of successful emails
- `emails_failed`: Count of failed emails
- `status`: 'success' or 'failed'

## Testing the System

### Test 1: Subscribe a New User
```bash
python test_subscription.py
```
Output should show:
- Form submission successful
- Message: "Check your email to verify your subscription"
- Verification email printed to Flask console

### Test 2: Verify Email Address
```bash
python test_verify.py
```
Output should show:
- 302 redirect to homepage
- "Subscriber should now be verified in database"

### Test 3: Check Database Status
```bash
python check_database.py
```
Output shows:
- List of all subscribers
- Their verification and active status
- All email logs with status

## Common Issues & Solutions

### Issue: "TimeoutError on port 587/465"
**Cause**: Gmail SMTP is blocked by network firewall (e.g., on NASA/corporate networks)

**Solution**: Set `SMTP_TESTING=True` in `.env` (already done)

**For real SMTP**: Deploy to cloud environment (AWS, Heroku, PythonAnywhere) where external SMTP is allowed

### Issue: "No verification link in email"
**Solution**: Check Flask server console output for the verification link. Copy it into browser.

### Issue: "Secret key error" when trying to verify
**Solution**: Verify `.env` has `SECRET_KEY=...` set and Flask is restarted

### Issue: "subscriber not verified after clicking link"
**Solution**: 
- Check that link includes correct token
- Verify Flask server is still running
- Check database with `python check_database.py`

## For Production Deployment

### Option 1: Cloud Platform with SMTP (Recommended)
1. Deploy to Heroku, AWS, or PythonAnywhere
2. Set `SMTP_TESTING=False` in production `.env`
3. Use Gmail app password (already configured)
4. Real emails will be sent automatically

### Option 2: Alternative Email Service
Replace Flask-Mail with SendGrid, Mailgun, or AWS SES:
```python
# Example with SendGrid
SENDGRID_API_KEY=your-api-key
```

### Option 3: Local SMTP Server
Run local mail server (Postfix, Exim) that forwards to Gmail

## Email Template Customization

Edit verification email in `app/routes.py` function `send_verification_email()`:
```python
html = f"""
<html>
    <!-- Customize this HTML for your branding -->
</html>
"""
```

Edit monthly KML email in `app/tasks.py` function `render_email_template()`:
```python
html = f"""
<html>
    <!-- Customize this HTML for your branding -->
</html>
"""
```

## Monthly KML Generation

Set schedule in `.env`:
```dotenv
KML_SCHEDULE_DAY=1        # Day of month (1-31)
KML_SCHEDULE_HOUR=9       # Hour (0-23 UTC)
KML_SCHEDULE_MINUTE=0     # Minute (0-59)
```

Schedule runs automatically via APScheduler when server is running.

## Support

For issues with email configuration:
1. Check Flask server console output
2. Verify database status with `python check_database.py`
3. Ensure `.env` file is properly configured
4. Check that Flask is running: `http://localhost:5000/`

---

**Last Updated**: February 18, 2026  
**Status**: ✅ Email system operational in development mode
