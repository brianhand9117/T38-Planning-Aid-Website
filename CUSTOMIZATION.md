# Customization Guide for T-38 Planning Aid Email Service

This guide explains how to customize the website to match your organization's branding and needs.

## Brand Customization

### 1. Logo and Title

Edit `app/templates/base.html`:

```html
<a href="{{ url_for('main.index') }}" class="logo">
    <span class="logo-text">🚀 Your Custom Title</span>
</a>
```

### 2. Colors

Edit `app/static/css/style.css` - Change the CSS variables at the top:

```css
:root {
    --primary-blue: #0B3D91;      /* Main blue */
    --secondary-blue: #1B4EC5;    /* Secondary blue */
    --accent-blue: #4A90E2;       /* Accent color */
    --nasa-red: #E63946;          /* Red accent */
    --success-green: #52B788;     /* Success color */
    /* ... add more customizations */
}
```

### 3. Footer Content

Edit `app/templates/base.html` footer section:

```html
<footer class="footer">
    <div class="container">
        <div class="footer-content">
            <div class="footer-section">
                <h5>Your Organization</h5>
                <p>Your custom description here</p>
            </div>
            <!-- More sections -->
        </div>
    </div>
</footer>
```

## Email Customization

### 1. Subscription Confirmation Email

Edit `app/routes.py` - `send_verification_email()` function:

```python
def send_verification_email(subscriber):
    """Send verification email to subscriber"""
    verify_url = url_for('main.verify_email', token=subscriber.verification_token, _external=True)
    
    html = f"""
    <html>
        <body>
            <!-- Customize HTML here -->
            <h2>Your Custom Subject</h2>
            <p>Your custom message</p>
        </body>
    </html>
    """
```

### 2. Monthly KML Email

Edit `app/tasks.py` - `render_email_template()` function:

```python
def render_email_template(subscriber_name, kml_gen):
    """Render the HTML email template for KML distribution"""
    html = f"""
    <html>
        <body>
            <!-- Customize the monthly email design here -->
        </body>
    </html>
    """
```

## Content Customization

### 1. Homepage Hero Section

Edit `app/templates/index.html`:

```html
<section class="hero">
    <div class="container hero-content">
        <h1 class="hero-title">Your Custom Title</h1>
        <p class="hero-subtitle">Your custom subtitle</p>
        <p class="hero-description">Your custom description</p>
    </div>
</section>
```

### 2. Features Section

Edit `app/templates/index.html` - Update feature cards:

```html
<div class="feature-card">
    <div class="feature-icon">📊</div>
    <h3>Your Feature Title</h3>
    <p>Your feature description</p>
</div>
```

### 3. About Page

Edit `app/templates/about.html` to customize content:

```html
<h2>Your Section Title</h2>
<p>Your content here</p>
<ul>
    <li>Your item 1</li>
    <li>Your item 2</li>
</ul>
```

### 4. Privacy Policy

Edit `app/templates/privacy.html` with your organization's privacy policy

### 5. Contact Information

Edit `app/routes.py` - `contact()` function to set your email:

```python
msg = Message(
    subject=f'Contact from {name}',
    recipients=['your-email@yourdomain.com'],  # Set your email here
    body=f'From: {email}\n\n{message}'
)
```

## Functionality Customization

### 1. Email Scheduling

Change when KML files are generated in `.env`:

```ini
# Generate on 15th at 2 PM UTC instead of 1st at 9 AM
KML_SCHEDULE_DAY=15
KML_SCHEDULE_HOUR=14
KML_SCHEDULE_MINUTE=0
```

### 2. Add Custom Fields to Subscribers

Edit `app/models.py` - Add fields to `Subscriber` model:

```python
class Subscriber(db.Model):
    # ... existing fields ...
    organization = db.Column(db.String(200))  # New field
    phone_number = db.Column(db.String(20))   # New field
```

Then update forms and templates to include these fields.

### 3. Add Admin Authentication

Create `app/auth.py`:

```python
from flask import session, redirect, url_for
from functools import wraps

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin' not in session:
            return redirect(url_for('main.login'))
        return f(*args, **kwargs)
    return decorated_function

# Add login route to routes.py
@main_bp.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    # Implement login logic
    pass
```

### 4. Add More Email Notifications

Edit `app/tasks.py` to send additional emails:

```python
def send_custom_email(subscriber):
    """Send custom email notification"""
    msg = Message(
        subject='Your Custom Subject',
        recipients=[subscriber.email],
        html='<p>Your HTML content</p>'
    )
    mail.send(msg)
```

## Database Customization

### 1. Add Custom Tables

Edit `app/models.py`:

```python
class CustomModel(db.Model):
    __tablename__ = 'custom_table'
    
    id = db.Column(db.Integer, primary_key=True)
    your_field = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

Then run:
```bash
# In Python shell
from app import db, create_app
app = create_app()
with app.app_context():
    db.create_all()
```

## Styling Customization

### 1. Change Fonts

Edit CSS in `app/static/css/style.css`:

```css
body {
    font-family: 'Your Font', sans-serif;  /* Change from Roboto */
}
```

### 2. Add Custom CSS Classes

Add to `app/static/css/style.css`:

```css
.my-custom-class {
    background-color: #your-color;
    padding: 2rem;
    border-radius: 8px;
}
```

### 3. Change Responsive Breakpoints

Edit media queries in `app/static/css/style.css`:

```css
@media (max-width: 1024px) {
    /* Your custom breakpoint style */
}
```

## API Customization

### 1. Add Custom Endpoints

Edit `app/routes.py`:

```python
@main_bp.route('/your-custom-endpoint')
def your_custom_endpoint():
    return render_template('your_template.html', data=your_data)
```

### 2. Add JSON API

```python
@main_bp.route('/api/subscribers', methods=['GET'])
def get_subscribers_api():
    subscribers = Subscriber.query.filter_by(is_active=True).all()
    return jsonify([{
        'email': s.email,
        'name': f"{s.first_name} {s.last_name}"
    } for s in subscribers])
```

## Security Customizations

### 1. Enable CSRF Protection

Add to `app/__init__.py`:

```python
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()
csrf.init_app(app)
```

### 2. Rate Limiting

Install: `pip install Flask-Limiter`

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@main_bp.route('/subscribe', methods=['POST'])
@limiter.limit("5 per minute")
def subscribe():
    # Limited to 5 subscriptions per minute per IP
    pass
```

### 3. User Authentication

Implement Flask-Login for admin access control

## Testing Customizations

Edit test files to test your customizations:

```bash
# Create tests/test_routes.py
def test_custom_endpoint():
    response = client.get('/your-custom-endpoint')
    assert response.status_code == 200
```

## Deployment Customizations

### 1. Environment-Specific Settings

Create `config.py`:

```python
class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
```

### 2. Docker Customization

Edit `Dockerfile` and `docker-compose.yml` for your deployment needs

## Support

For questions about customizations, refer to:
- Flask Documentation: https://flask.palletsprojects.com/
- SQLAlchemy: https://docs.sqlalchemy.org/
- HTML/CSS Guides: https://developer.mozilla.org/

---

**Happy customizing!** 🎨
