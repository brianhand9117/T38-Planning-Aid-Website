# Quick Start Guide - T-38 Planning Aid Email Service

Get your website up and running in 5 minutes!

## Step 1: (2 minutes) Create Environment File

Create a file named `.env` in the `website/` directory:

```bash
# Windows
type nul > .env

# macOS/Linux
touch .env
```

## Step 2: (1 minute) Configure Email

Edit `.env` and add your email settings. Choose one option:

### Option A: Gmail (Easiest)

```ini
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=T38 Planning Aid <your-email@gmail.com>
```

**Steps to get App Password:**
1. Go to https://myaccount.google.com/apppasswords
2. Select "Mail" and "Windows Computer"
3. Copy the generated 16-character password
4. Paste it as `MAIL_PASSWORD` in `.env`

### Option B: Outlook

```ini
MAIL_SERVER=smtp-mail.outlook.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@outlook.com
MAIL_PASSWORD=your-password
MAIL_DEFAULT_SENDER=T38 Planning Aid <your-email@outlook.com>
```

## Step 3: (1 minute) Add Other Settings

Add these required settings to `.env`:

```ini
# Database
SQLALCHEMY_DATABASE_URI=sqlite:///t38_email.db

# Schedule: Monthly on 1st at 9 AM UTC
KML_SCHEDULE_DAY=1
KML_SCHEDULE_HOUR=9
KML_SCHEDULE_MINUTE=0

# Path to your T-38 repository
KML_REPO_PATH=../
```

## Step 4: (1 minute) Install & Launch

```bash
# 1. Navigate to website directory
cd website

# 2. Create virtual environment
python -m venv venv

# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python run.py
```

## Step 5: Open Website

Visit: **http://localhost:5000**

## What You Get

✅ Public homepage with subscription form
✅ NASA-themed design
✅ Admin dashboard at `http://localhost:5000/admin/dashboard`
✅ Database for subscribers
✅ Monthly email scheduling
✅ Email verification system

## Next Steps

1. **Test Subscription**:
   - Go to homepage
   - Enter your email
   - Check email for verification link

2. **Check Admin**:
   - Visit `/admin/dashboard`
   - See subscriber and email statistics

3. **Manual Test** (Optional):
   - Edit `app/tasks.py` to test KML generation
   - Run the monthly job manually for testing

4. **Deploy** (When ready):
   - Use Heroku, DigitalOcean, AWS, or your own server
   - See `README.md` for deployment guides

## Common Issues

### "Module not found" error
```bash
# Make sure virtual environment is activated
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate
```

### Email not sending
```bash
# Check your .env file has correct credentials
# For Gmail: Verify App Password was generated correctly
# Test connection: python -c "import smtplib; smtplib.SMTP('smtp.gmail.com', 587)"
```

### Port 5000 already in use
```bash
# Change port in .env:
FLASK_PORT=5001  # or any available port
```

## Support

See the main `README.md` for detailed configuration and troubleshooting.

---

**Congratulations!** Your T-38 Planning Aid Email Service is running! 🚀
