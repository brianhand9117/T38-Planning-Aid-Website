# T-38 Planning Aid - Email Subscription Website

A NASA-themed web application that allows users to subscribe to monthly email updates containing the latest T-38 Planning Aid KML files for flight planning.

## 🚀 Features

- **NASA-Themed UI**: Beautiful responsive design with NASA blue color scheme
- **Email Subscription**: Users can subscribe with verification workflow
- **Monthly Automation**: Automatically generates and distributes KML files to verified subscribers
- **Admin Dashboard**: View subscribers, email logs, and KML generation history
- **Database Tracking**: SQLite database with email logs and subscriber management
- **Development Mode**: Console-based email testing when SMTP is unavailable
- **Docker Support**: Included Dockerfile for easy deployment

## 📋 Prerequisites

- Python 3.9+
- pip or poetry for dependency management
- Gmail account with app password (for production email sending)
- Git (for version control)

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/brianhand9117/T38-Planning-Aid-Website.git
cd T38-Planning-Aid-Website
```

### 2. Create Virtual Environment
```bash
python -m venv venv
```

#### Activate Virtual Environment:
**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
Create a `.env` file in the root directory:
```bash
cp .env.example .env
```

Edit `.env` with your settings:
```dotenv
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-change-in-production

# Database
SQLALCHEMY_DATABASE_URI=sqlite:///t38_email.db

# Email Configuration
SMTP_TESTING=True                    # Set to False for real Gmail SMTP
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=465
MAIL_USE_SSL=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password      # Gmail app password, not regular password
MAIL_DEFAULT_SENDER=T38 Planning Aid <your-email@gmail.com>

# KML Repository Path
KML_REPO_PATH=../                    # Adjust to point to T-38 Planning Aid repo
```

## 🏃 Running the Application

```bash
python run.py
```

The application will be available at `http://localhost:5000/`

### Admin Dashboard
Access at: `http://localhost:5000/admin/` (no authentication in development)

## 📧 Email Configuration

### For Development (SMTP_TESTING=True)
- Emails appear in Flask server console
- Perfect for testing on networks where Gmail SMTP is blocked
- All emails are logged to database

### For Production (SMTP_TESTING=False)
1. Create a Gmail app password:
   - Go to myaccount.google.com → Security
   - Enable 2-Factor Authentication
   - Create App Password (16 character code)
   - Use this in MAIL_PASSWORD field

2. Update .env:
   ```
   SMTP_TESTING=False
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-16-char-app-password
   ```

3. Deploy to cloud environment (Heroku, AWS, etc) where SMTP is allowed

## 🧪 Testing

### Test Subscription
```bash
python test_subscription.py
```

### Test Email Verification
```bash
python test_verify.py
```

### Check Database Status
```bash
python check_database.py
```

### Get Verification Link for Email
```bash
python get_verify_link.py
```

## 📚 Documentation

- **[README.md](README.md)** - Overview and quick start
- **[QUICKSTART.md](QUICKSTART.md)** - Step-by-step setup guide
- **[EMAIL_TROUBLESHOOTING.md](EMAIL_TROUBLESHOOTING.md)** - Email system troubleshooting and development guide
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Production deployment instructions
- **[CUSTOMIZATION.md](CUSTOMIZATION.md)** - Customizing the application
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Technical architecture overview

## 🗂️ Project Structure

```
T38-Planning-Aid-Website/
├── app/
│   ├── __init__.py           # Flask app factory, extensions
│   ├── models.py             # Database models (Subscriber, EmailLog, KMLGeneration)
│   ├── routes.py             # Flask routes and views
│   ├── tasks.py              # Background jobs and schedulers
│   ├── static/
│   │   ├── css/style.css     # NASA-themed styling
│   │   └── js/main.js        # Frontend JavaScript
│   └── templates/
│       ├── base.html         # Base template with header/footer
│       ├── index.html        # Homepage with subscription form
│       ├── about.html        # About page
│       ├── contact.html      # Contact page
│       ├── privacy.html      # Privacy policy
│       └── admin/
│           ├── dashboard.html      # Admin dashboard
│           ├── subscribers.html    # Subscriber management
│           ├── emails.html         # Email log viewer
│           └── kml_history.html    # KML generation history
├── run.py                    # Flask application entry point
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
├── .gitignore               # Git ignore rules
├── Dockerfile               # Docker container configuration
├── docker-compose.yml       # Docker Compose setup
└── [documentation files]    # README, guides, etc.
```

## 🗄️ Database Schema

### Subscriber Table
- `id`: Primary key
- `email`: Unique email address
- `first_name`, `last_name`: Subscriber name
- `is_active`: Subscription active flag
- `is_verified`: Email verification status
- `verification_token`: Token for verification link
- `subscribed_date`: Subscription timestamp
- `unsubscribed_date`: Unsubscription timestamp (if applicable)

### EmailLog Table
- `id`: Primary key
- `subscriber_id`: Foreign key to Subscriber
- `subject`: Email subject line
- `kml_filename`: Name of attached KML file
- `status`: 'sent', 'failed', or 'pending'
- `error_message`: Error details if failed
- `sent_date`: Timestamp

### KMLGeneration Table
- `id`: Primary key
- `filename`: Generated KML file name
- `filepath`: Full path to file
- `file_size_mb`: File size in MB
- `generation_date`: Generation timestamp
- `emails_sent`: Count of successful emails
- `emails_failed`: Count of failed emails
- `status`: 'success' or 'failed'

## 🔄 Monthly KML Distribution

The application automatically runs a scheduled job on the 1st of each month at 9 AM UTC:

1. **Generates** the latest KML file from T-38 Planning Aid data
2. **Sends** the KML file to all verified subscribers
3. **Logs** all email attempts to the database

### Configure Schedule
Edit `.env`:
```dotenv
KML_SCHEDULE_DAY=1       # Day of month (1-31)
KML_SCHEDULE_HOUR=9      # Hour UTC (0-23)
KML_SCHEDULE_MINUTE=0    # Minute (0-59)
```

## 🐳 Docker Deployment

Build and run with Docker:
```bash
docker-compose up -d
```

Application will be available at `http://localhost:5000/`

## 🚀 Deployment Options

### Cloud Platforms
- **Heroku**: Easy 1-click deployment with Flask apps
- **PythonAnywhere**: Python hosting with email support
- **AWS**: Full control with EC2 instances
- **DigitalOcean**: Affordable VPS hosting

### Steps to Deploy
1. See [DEPLOYMENT.md](DEPLOYMENT.md) for platform-specific instructions
2. Update production `.env` file
3. Set `SMTP_TESTING=False` for real email
4. Deploy database migrations
5. Configure domain and HTTPS

## 📝 Customization

Edit email templates and styling:
- Email verification template: `app/routes.py` → `send_verification_email()`
- Monthly KML email template: `app/tasks.py` → `render_email_template()`
- Website styling: `app/static/css/style.css`
- HTML pages: `app/templates/*.html`

See [CUSTOMIZATION.md](CUSTOMIZATION.md) for detailed instructions.

## 🐛 Troubleshooting

### Email Issues
See [EMAIL_TROUBLESHOOTING.md](EMAIL_TROUBLESHOOTING.md) for:
- SMTP connection problems
- Gmail authentication issues
- Testing email delivery
- Development vs production modes

### Database Issues
```bash
# Reset database (careful - loses all data!)
rm t38_email.db
python run.py  # Will recreate with schema
```

### Port Already in Use
```bash
# Change port in .env
FLASK_PORT=5001
```

## 📧 Contact & Support

For issues:
1. Check [EMAIL_TROUBLESHOOTING.md](EMAIL_TROUBLESHOOTING.md)
2. Review [DEPLOYMENT.md](DEPLOYMENT.md) for setup issues
3. Open an issue on GitHub
4. Contact: brianhand54@gmail.com

## 📄 License

This project is provided as-is for the T-38 Planning Aid community.

## 🙏 Acknowledgments

- NASA for inspiration and mission
- USAF T-38 Talon community
- Flask, SQLAlchemy, and APScheduler teams

---

**Last Updated**: February 18, 2026  
**Status**: ✅ Production-ready with development mode support
