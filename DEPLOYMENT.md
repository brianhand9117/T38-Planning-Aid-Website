# Deployment Guide - T-38 Planning Aid Email Service

Complete instructions for deploying your website to production.

## Pre-Deployment Checklist

- [ ] `.env` file configured with your email settings
- [ ] Password strength verified for email account
- [ ] Database tested locally
- [ ] All tests passing
- [ ] Security settings reviewed
- [ ] Domain name secured (if needed)
- [ ] SSL/TLS certificate ready

## Local Deployment (Development Server)

### Using Flask Development Server

```bash
python run.py
```

⚠️ **Not recommended for production** - Use Gunicorn instead.

### Using Gunicorn (Better for Production)

```bash
# Install gunicorn
pip install gunicorn

# Run with 4 workers
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"

# Run in background with logs
gunicorn -w 4 -b 0.0.0.0:5000 --access-logfile access.log --error-logfile error.log "app:create_app()" &
```

## Heroku Deployment

### Step 1: Install Heroku CLI

Download from: https://devcenter.heroku.com/articles/heroku-cli

### Step 2: Login to Heroku

```bash
heroku login
```

### Step 3: Create Git Repository (if not already)

```bash
cd /path/to/Hand-T38_Planning_Aid-Fork
git init
git add .
git commit -m "Initial commit"
```

### Step 4: Create Heroku App

```bash
heroku create your-app-name
# Example: heroku create t38-planning-aid
```

### Step 5: Set Environment Variables

```bash
heroku config:set MAIL_SERVER=smtp.gmail.com
heroku config:set MAIL_PORT=587
heroku config:set MAIL_USE_TLS=True
heroku config:set MAIL_USERNAME=your-email@gmail.com
heroku config:set MAIL_PASSWORD=your-app-password
heroku config:set MAIL_DEFAULT_SENDER="T38 Planning Aid <your-email@gmail.com>"
heroku config:set FLASK_ENV=production
heroku config:set KML_REPO_PATH=../
```

### Step 6: Create/Update Procfile

```
web: gunicorn -w 4 "app:create_app('production')"
worker: python run.py
```

### Step 7: Create runtime.txt

```
python-3.9.16
```

### Step 8: Deploy

```bash
git push heroku main
```

### Step 9: Create Database

```bash
heroku run python -c "from app import create_app, db; app = create_app(); db.create_all()"
```

### Step 10: View Logs

```bash
heroku logs --tail
```

### Step 11: Open Website

```bash
heroku open
```

Or visit: `https://your-app-name.herokuapp.com`

### Heroku Tips

- **Use Postgres for Production**:
  ```bash
  heroku addons:create heroku-postgresql:hobby-dev
  # Update SQLALCHEMY_DATABASE_URI in .env
  ```

- **Scheduled Tasks on Heroku**:
  - Use Heroku Scheduler add-on for monthly KML generation
  - Or use APScheduler (already included)

- **Monitor App Health**:
  ```bash
  heroku ps
  heroku metrics
  ```

## DigitalOcean Deployment

### Step 1: Create Droplet

1. Visit https://cloud.digitalocean.com
2. Create new Droplet
3. Select:
   - **Image**: Ubuntu 20.04 LTS
   - **Size**: $5-10/month (sufficient for this app)
   - **Region**: Your nearby region
4. Add SSH key or password
5. Create Droplet

### Step 2: Connect to Droplet

```bash
ssh root@your_droplet_ip
```

### Step 3: Install Dependencies

```bash
apt update && apt upgrade -y
apt install -y python3 python3-pip python3-venv git nginx supervisor

# Install database support (optional)
apt install -y postgresql postgresql-contrib
```

### Step 4: Clone Repository

```bash
cd /home
git clone https://github.com/brianhand9117/Hand-T38_Planning_Aid-Fork.git
cd Hand-T38_Planning_Aid-Fork/website
```

### Step 5: Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

### Step 6: Configure Environment

```bash
nano .env
# Add your configuration here
```

### Step 7: Create Supervisor Configuration

```bash
nano /etc/supervisor/conf.d/t38_planning_aid.conf
```

Add:

```ini
[program:t38_planning_aid]
directory=/home/Hand-T38_Planning_Aid-Fork/website
command=/home/Hand-T38_Planning_Aid-Fork/website/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 "app:create_app('production')"
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/t38_planning_aid.log
```

### Step 8: Configure Nginx

```bash
nano /etc/nginx/sites-available/t38_planning_aid
```

Add:

```nginx
server {
    listen 80;
    server_name your_domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Step 9: Enable Nginx

```bash
ln -s /etc/nginx/sites-available/t38_planning_aid /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

### Step 10: Start Application

```bash
supervisorctl reread
supervisorctl update
supervisorctl start t38_planning_aid
supervisorctl status
```

### Step 11: Setup HTTPS (SSL)

```bash
apt install -y certbot python3-certbot-nginx
certbot --nginx -d your_domain.com
```

## AWS Deployment

### Option 1: AWS Elastic Beanstalk (Recommended)

1. Install EB CLI:
```bash
pip install awsebcli
```

2. Initialize Elastic Beanstalk:
```bash
eb init -p python-3.9 t38-planning-aid
```

3. Create `.ebextensions/python.config`:
```yaml
option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: "wsgi.py"
  aws:autoscaling:launchconfiguration:
    IamInstanceProfile: aws-elasticbeanstalk-ec2-role
```

4. Create `wsgi.py`:
```python
from app import create_app

app = create_app('production')

if __name__ == "__main__":
    app.run()
```

5. Deploy:
```bash
eb create t38-planning-aid-env
eb setenv MAIL_SERVER=smtp.gmail.com MAIL_USERNAME=... MAIL_PASSWORD=...
eb deploy
```

### Option 2: AWS EC2 (Manual)

1. Launch EC2 instance (Ubuntu 20.04)
2. Follow DigitalOcean steps above
3. Use RDS for database (optional)
4. Use SES for email (optional)

## Docker Deployment

### Build Image

```bash
cd website
docker build -t t38-planning-aid .
```

### Run Container

```bash
docker run -d \
  -p 5000:5000 \
  -e MAIL_SERVER=smtp.gmail.com \
  -e MAIL_USERNAME=your-email \
  -e MAIL_PASSWORD=your-password \
  --name t38-planning-aid \
  t38-planning-aid
```

### Using Docker Compose

```bash
# Create .env file with your settings
docker-compose up -d
```

## HTTPS/SSL Setup

### Using Let's Encrypt (Free)

#### On Linux Server:

```bash
# Install Certbot
apt install -y certbot python3-certbot-nginx

# Generate certificate
certbot certonly --standalone -d your-domain.com

# Configure Nginx with SSL (see DigitalOcean section above)
```

#### On Heroku:

1. Use Heroku Automated Certificate Management (ACM)
2. Or use third-party SSL provider

#### On AWS:

1. Use AWS Certificate Manager (ACM)
2. Or import from Let's Encrypt

## Monitoring & Maintenance

### Log Monitoring

```bash
# Heroku
heroku logs --tail

# DigitalOcean/Linux
tail -f /var/log/t38_planning_aid.log

# Docker
docker logs -f t38-planning-aid
```

### Performance Monitoring

Monitor with:
- New Relic
- Datadog
- CloudWatch (AWS)

### Backups

```bash
# Backup database
sqlite3 t38_email.db ".dump" > backup_$(date +%Y%m%d).sql

# Or use cloud backup services
```

### Updates

```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Restart application
# (Depends on deployment method)
```

## Troubleshooting Deployment

### Website Not Loading

1. Check server status:
   ```bash
   heroku ps          # Heroku
   supervisorctl status  # DigitalOcean
   docker ps          # Docker
   ```

2. Check logs
3. Verify environment variables are set
4. Check firewall settings

### Email Not Sending

1. Verify `MAIL_SERVER` and `MAIL_PORT` in logs
2. Test SMTP connection:
   ```bash
   python -c "import smtplib; s = smtplib.SMTP('smtp.gmail.com', 587); s.starttls()"
   ```
3. Check email credentials
4. Verify firewall allows port 587

### Database Issues

1. Check database permissions
2. Verify database connection string
3. Run migrations if applicable

### Memory Issues

1. Increase Dyno size (Heroku) or Droplet size
2. Optimize code for memory usage
3. Use CDN for static files

## Cost Comparison

| Platform | Monthly Cost | Notes |
|----------|-------------|-------|
| Heroku | $7-50+ | Auto-scaling, easy deployment |
| DigitalOcean | $5-10+ | VPS, manual scaling |
| AWS | Variable | Complex, more expensive |
| Self-hosted | Hardware | One-time hardware cost |

## Recommended Setup

For most users:
- **Small to Medium**: DigitalOcean ($5/month)
- **Professional**: Heroku ($7-50/month)
- **Enterprise**: AWS with RDS and CloudFront

---

**Need help?** Check the main README.md or community resources for your chosen platform.
