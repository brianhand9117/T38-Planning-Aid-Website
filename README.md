# T-38 Planning Aid - Email Service Website

A NASA-themed Flask web application that allows users to subscribe to monthly KML file updates containing current T-38 aircraft operational airport data. The website automatically generates KML files from your existing T-38 Planning Aid code and distributes them via email to subscribers.

## Features

- **🌐 NASA-Themed Design**: Professional, modern interface with NASA-inspired color scheme
- **📧 Email Subscriptions**: Users can subscribe to receive monthly KML file updates
- **🔒 Email Verification**: Double opt-in subscription system for data protection
- **📅 Automated Scheduling**: Monthly KML generation and email distribution on configurable schedule
- **📊 Admin Dashboard**: Manage subscribers, view email logs, and track KML generation history
- **🔌 Integration**: Seamlessly integrates with your existing T-38 Planning Aid code
- **📱 Responsive Design**: Works perfectly on desktop, tablet, and mobile devices

## Prerequisites

- Python 3.8 or higher
- Your existing T-38 Planning Aid repository (GUI Files folder)
- Email account (Gmail, Outlook, or custom SMTP server)

## Installation

### 1. Clone the Website

```bash
# Navigate to your T-38 Planning Aid repository
cd /path/to/Hand-T38_Planning_Aid-Fork

# Files are already in the /website directory
cd website
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your settings
# See Configuration section below
```

## Configuration

### Environment Variables (.env)

Create a `.env` file in the `website` directory with the following settings:

```ini
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_HOST=0.0.0.0
FLASK_PORT=5000

# Database
SQLALCHEMY_DATABASE_URI=sqlite:///t38_email.db

# Email Configuration (Gmail Example)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=T38 Planning Aid <your-email@gmail.com>

# KML Generation Schedule (cron format)
# Monthly on the 1st at 9 AM UTC
KML_SCHEDULE_DAY=1
KML_SCHEDULE_HOUR=9
KML_SCHEDULE_MINUTE=0

# KML Repository Path
KML_REPO_PATH=../
```

### Email Configuration Options

#### Gmail (Recommended)

1. Enable 2-Factor Authentication on your Google account
2. Generate an App Password: https://myaccount.google.com/apppasswords
3. Use the generated password in `MAIL_PASSWORD`

```ini
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-16-character-app-password
MAIL_DEFAULT_SENDER=T38 Planning Aid <your-email@gmail.com>
```

#### Outlook/Microsoft

```ini
MAIL_SERVER=smtp-mail.outlook.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@outlook.com
MAIL_PASSWORD=your-password
MAIL_DEFAULT_SENDER=T38 Planning Aid <your-email@outlook.com>
```

#### Custom SMTP Server

```ini
MAIL_SERVER=your-smtp-server.com
MAIL_PORT=587  # or 25, 465 depending on your server
MAIL_USE_TLS=True  # or False if using SSL
MAIL_USERNAME=your-username
MAIL_PASSWORD=your-password
MAIL_DEFAULT_SENDER=T38 Planning Aid <noreply@yourdomain.com>
```

## Running the Application

### Development Mode

```bash
python run.py
```

The website will be available at `http://localhost:5000`

### Production Mode

For production deployment, use a production WSGI server:

```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
```

### Docker Mode (Recommended for Production)

The application includes a **multi-container Docker setup** that separates the web server from the background scheduler for autonomous operation.

**Quick Start:**

```bash
# 1. Create .env file with your configuration
cp .env.example .env
# Edit .env with your email settings

# 2. Build and start services
docker compose up -d

# 3. View logs
docker compose logs -f
```

**Services:**
- **Web Service**: Flask app with Gunicorn (port 5000)
- **Worker Service**: APScheduler for background tasks
- **Shared Database**: SQLite database via Docker volumes

**Benefits:**
- ✅ Scheduler runs 24/7 independently from web server
- ✅ Web server can restart without losing scheduled jobs
- ✅ Production-ready with health checks and auto-restart
- ✅ Easy to scale and monitor

📖 **Full Docker documentation:** See [DOCKER_SETUP.md](DOCKER_SETUP.md) for complete guide

## Project Structure

```
website/
├── run.py                  # Application entry point (development)
├── worker.py               # Worker process for APScheduler (production)
├── requirements.txt        # Python dependencies
├── .env.example           # Example environment configuration
├── Dockerfile             # Docker image configuration
├── docker-compose.yml     # Multi-container Docker setup
├── DOCKER_SETUP.md        # Complete Docker documentation
├── app/
│   ├── __init__.py        # Flask app factory and configuration
│   ├── models.py          # Database models
│   ├── routes.py          # Flask routes (public & admin)
│   ├── tasks.py           # Background tasks & scheduler
│   ├── templates/         # HTML templates
│   │   ├── base.html      # Base template with NASA theme
│   │   ├── index.html     # Homepage with subscription form
│   │   ├── about.html     # About page
│   │   ├── privacy.html   # Privacy policy
│   │   ├── contact.html   # Contact form
│   │   └── admin/         # Admin dashboard templates
│   │       ├── dashboard.html
│   │       ├── subscribers.html
│   │       ├── emails.html
│   │       └── kml_history.html
│   └── static/
│       ├── css/
│       │   └── style.css  # NASA-themed stylesheet
│       ├── js/
│       │   └── main.js    # Frontend JavaScript
│       └── images/        # Images directory
└── t38_email.db          # SQLite database (created on first run)
```

## Database Models

### Subscriber

Stores email subscription information:
- `email`: Subscriber's email address (unique)
- `first_name`, `last_name`: Subscriber's name
- `is_active`: Whether subscription is active
- `is_verified`: Email verification status
- `verification_token`: Token for email verification
- `subscribed_date`: When subscriber joined
- `unsubscribed_date`: When subscriber left (if applicable)

### EmailLog

Tracks sent emails:
- `subscriber_id`: Reference to subscriber
- `subject`: Email subject line
- `sent_date`: When email was sent
- `kml_filename`: Name of attached KML file
- `status`: 'sent', 'bounced', or 'failed'
- `error_message`: Error details if failed

### KMLGeneration

Tracks KML file generation:
- `generation_date`: When KML was generated
- `filename`: Generated filename
- `filepath`: Full path to KML file
- `file_size_mb`: File size in megabytes
- `num_airports`: Number of airports in KML
- `status`: 'success' or 'failed'
- `emails_sent`: Number of successful email sends
- `emails_failed`: Number of failed email sends

## API Routes

### Public Routes

- `GET /` - Home page with subscription form
- `POST /subscribe` - Subscribe to mailing list
- `GET /verify/<token>` - Verify email subscription
- `GET /unsubscribe/<token>` - Unsubscribe from mailing list
- `GET /about` - About page
- `GET /privacy` - Privacy policy
- `GET /contact` - Contact form (GET and POST)

### Admin Routes

- `GET /admin/dashboard` - Admin dashboard with statistics
- `GET /admin/subscribers` - Manage subscribers (paginated)
- `GET /admin/emails` - View email logs (paginated)
- `GET /admin/kml-history` - View KML generation history (paginated)

## Scheduled Tasks

### Monthly KML Generation

By default, the application generates KML files and sends emails on the 1st of every month at 9 AM UTC.

To change the schedule, modify `.env`:

```ini
# Generate on the 15th at 2 PM UTC
KML_SCHEDULE_DAY=15
KML_SCHEDULE_HOUR=14
KML_SCHEDULE_MINUTE=0
```

## Integration with T-38 Planning Aid

The website automatically integrates with your existing T-38 Planning Aid code:

1. **KML Generation**: Calls the GUI script to generate KML files
2. **File Distribution**: Attaches the KML file to emails
3. **Data Synchronization**: Uses the same data sources as the desktop application

The `KML_REPO_PATH` environment variable should point to your T-38 Planning Aid repository root.

## Troubleshooting

### Email Not Sending

1. **Check email credentials**:
   - Verify `MAIL_USERNAME` and `MAIL_PASSWORD` in `.env`
   - For Gmail, ensure you've generated an App Password
   - Test SMTP connection manually

2. **Check SMTP settings**:
   ```bash
   python -c "
   from flask_mail import Mail, Message
   from app import create_app
   app = create_app()
   with app.app_context():
       test_msg = Message('Test', recipients=['test@example.com'], body='Test')
       # This will print connection details
   "
   ```

3. **Review logs**: Check the console output for Flask error messages

### KML Not Generating

1. **Verify path**: Check `KML_REPO_PATH` points to correct location
2. **Check dependencies**: Ensure all T-38 Planning Aid dependencies are installed
3. **Manual test**: Try running the GUI script directly to identify issues

### Database Issues

1. **Reset database**:
   ```bash
   rm t38_email.db
   python run.py  # Will recreate database
   ```

2. **Check permissions**: Ensure write permissions in website directory

## Deployment

### Heroku

1. Create `Procfile`:
```
web: gunicorn -w 4 -b 0.0.0.0:$PORT "app:create_app('production')"
worker: python run.py
```

2. Create `runtime.txt`:
```
python-3.9.16
```

3. Deploy:
```bash
heroku create your-app-name
git push heroku main
```

### AWS / DigitalOcean / Other

See deployment guides in [Flask documentation](https://flask.palletsprojects.com/deployment/)

## Security Notes

1. **Email Privacy**: All subscriber emails are stored encrypted
2. **HTTPS**: Always use HTTPS in production
3. **.env File**: Never commit `.env` to version control
4. **Admin Access**: Implement authentication for admin pages
5. **Rate Limiting**: Consider adding rate limiting to subscription form

## Development

### Running Tests

```bash
# Create test database
python -c "from app import db, create_app; app = create_app('testing'); db.create_all()"

# Run tests
pytest
```

### Adding New Features

1. Update models in `app/models.py` if needed
2. Create routes in `app/routes.py`
3. Add templates in `app/templates/`
4. Add styles to `app/static/css/style.css`

## Support & Feedback

For issues, feature requests, or feedback about this website application, please:

1. Check the troubleshooting section above
2. Review Flask documentation: https://flask.palletsprojects.com/
3. Contact your T-38 Planning Aid administrator

## License

This web application is distributed under the same license as the T-38 Planning Aid project.

## Credits

- **Design**: NASA-inspired theme (no official NASA affiliation)
- **Framework**: Flask web framework
- **Database**: SQLAlchemy ORM
- **Email**: Flask-Mail extension
- **Scheduling**: APScheduler background task scheduler
- **Integration**: T-38 Planning Aid by [Original Authors]

## Changelog

### Version 1.0.0 (Initial Release)
- Launch public website with subscription functionality
- Implement monthly KML email distribution
- Create admin dashboard
- NASA-themed responsive design
- Full integration with T-38 Planning Aid code
