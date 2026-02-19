# Docker Setup Guide - T-38 Planning Aid Email Service

## Overview

The T-38 Planning Aid Email Service uses a **multi-container Docker architecture** that separates the web server from the background task scheduler, enabling true autonomous operation.

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Docker Compose Setup                      │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐        ┌──────────────┐                   │
│  │  Web Service │        │ Worker Service│                   │
│  │   (Gunicorn) │        │ (APScheduler) │                   │
│  └──────┬───────┘        └───────┬───────┘                   │
│         │                        │                           │
│         └────────┬───────────────┘                           │
│                  │                                           │
│         ┌────────▼─────────┐                                 │
│         │  Shared Database │                                 │
│         │   (SQLite)       │                                 │
│         └──────────────────┘                                 │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### Components

1. **Web Service** (`t38-planning-aid-web`)
   - Runs Flask application with Gunicorn WSGI server
   - Handles HTTP requests and serves the website
   - Does NOT run the scheduler (delegated to worker)
   - Exposes port 5000 for web access

2. **Worker Service** (`t38-planning-aid-worker`)
   - Runs APScheduler independently
   - Handles scheduled KML generation and email distribution
   - Runs 24/7 independently from web server
   - No port exposure (background process)

3. **Database Init Service** (`t38-planning-aid-db-init`)
   - One-time initialization service
   - Creates database tables on first run
   - Exits after initialization

### Benefits

✅ **Autonomous Operation**: Scheduler runs independently from web server  
✅ **High Availability**: Web server can restart without losing scheduled jobs  
✅ **Scalability**: Services can be scaled independently  
✅ **Monitoring**: Separate logs for web and worker services  
✅ **Production-Ready**: Ready for cloud deployment (Heroku, AWS, DigitalOcean)  

## Quick Start

### Prerequisites

- Docker installed (version 20.10+)
- Docker Compose v2 installed
- `.env` file with configuration (see below)

### 1. Create Environment Configuration

Create a `.env` file in the project root:

```bash
# Flask Configuration
FLASK_ENV=production
FLASK_DEBUG=False

# Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USE_SSL=False
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=T38 Planning Aid <your-email@gmail.com>

# KML Generation Schedule (cron format)
KML_SCHEDULE_DAY=1
KML_SCHEDULE_HOUR=9
KML_SCHEDULE_MINUTE=0

# KML Repository
KML_REPO_PATH=../
```

### 2. Build and Start Services

```bash
# Build images
docker compose build

# Start all services
docker compose up -d

# View logs
docker compose logs -f
```

### 3. Verify Services

```bash
# Check service status
docker compose ps

# Expected output:
# NAME                       STATUS    PORTS
# t38-planning-aid-web       Up        0.0.0.0:5000->5000/tcp
# t38-planning-aid-worker    Up        
# t38-planning-aid-db-init   Exited (0)
```

### 4. Access the Application

Open your browser and navigate to:
```
http://localhost:5000
```

## Service Management

### Start Services

```bash
# Start all services
docker compose up -d

# Start specific service
docker compose up -d web
docker compose up -d worker
```

### Stop Services

```bash
# Stop all services
docker compose down

# Stop specific service
docker compose stop web
docker compose stop worker
```

### View Logs

```bash
# All services
docker compose logs -f

# Web service only
docker compose logs -f web

# Worker service only
docker compose logs -f worker

# Last 100 lines
docker compose logs --tail=100 worker
```

### Restart Services

```bash
# Restart all
docker compose restart

# Restart specific service
docker compose restart web
docker compose restart worker
```

### Check Service Health

```bash
# View service status
docker compose ps

# Inspect health checks
docker inspect t38-planning-aid-web | grep -A 10 Health
docker inspect t38-planning-aid-worker | grep -A 10 Health
```

## Configuration

### Environment Variables

All configuration is done through environment variables in the `.env` file:

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `FLASK_ENV` | Environment mode | `production` | No |
| `FLASK_DEBUG` | Enable debug mode | `False` | No |
| `MAIL_SERVER` | SMTP server | `smtp.gmail.com` | Yes |
| `MAIL_PORT` | SMTP port | `587` | Yes |
| `MAIL_USE_TLS` | Use TLS | `True` | Yes |
| `MAIL_USE_SSL` | Use SSL | `False` | Yes |
| `MAIL_USERNAME` | Email username | - | Yes |
| `MAIL_PASSWORD` | Email password | - | Yes |
| `MAIL_DEFAULT_SENDER` | Default sender | - | Yes |
| `KML_SCHEDULE_DAY` | Day of month (1-31) | `1` | No |
| `KML_SCHEDULE_HOUR` | Hour (0-23) | `9` | No |
| `KML_SCHEDULE_MINUTE` | Minute (0-59) | `0` | No |
| `KML_REPO_PATH` | T-38 code path | `../` | No |

### Volumes

The setup uses Docker volumes for persistence:

```yaml
volumes:
  db_data:       # SQLite database storage
  logs:          # Application logs
```

To view volume details:
```bash
docker volume ls
docker volume inspect t38-planning-aid-website_db_data
```

### Networks

Services communicate via a dedicated bridge network:
```bash
docker network inspect t38-planning-aid-website_t38-network
```

## Monitoring

### Check Scheduler Status

```bash
# View worker logs to see scheduled jobs
docker compose logs worker | grep "Scheduled jobs"

# Example output:
# worker  | Scheduled jobs: 1
# worker  |   - Job: Monthly KML Generation and Email Distribution (ID: monthly_kml_generation)
# worker  |     Next run: 2024-03-01 09:00:00
```

### Monitor Database

```bash
# Access database volume
docker compose exec web bash
# Inside container:
sqlite3 /app/data/t38_email.db
```

### View Application Logs

```bash
# Web server logs
docker compose exec web tail -f /app/logs/web.log

# Worker logs
docker compose exec worker tail -f /app/logs/worker.log
```

## Troubleshooting

### Web Service Won't Start

```bash
# Check logs
docker compose logs web

# Common issues:
# - Port 5000 already in use
# - Missing environment variables
# - Database connection issues
```

### Worker Service Won't Start

```bash
# Check logs
docker compose logs worker

# Common issues:
# - Database not initialized
# - Invalid schedule configuration
# - Missing email credentials
```

### Database Issues

```bash
# Reset database
docker compose down
docker volume rm t38-planning-aid-website_db_data
docker compose up -d
```

### Email Sending Issues

```bash
# Check worker logs for email errors
docker compose logs worker | grep -i "email\|smtp\|mail"

# Test email configuration
docker compose exec worker python -c "from flask_mail import Mail, Message; print('Mail module OK')"
```

## Development vs Production

### Development Mode (Local Testing)

Use `run.py` directly for development:

```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Run development server (includes scheduler)
python run.py
```

### Production Mode (Docker)

Use Docker Compose for production:
- Web server uses Gunicorn (4 workers)
- Scheduler runs in separate worker container
- Automatic restarts on failure
- Health checks enabled

## Scaling

### Scale Web Service

```bash
# Run 3 web server instances
docker compose up -d --scale web=3
```

**Note**: Only scale the web service. The worker service should run as a single instance to avoid duplicate scheduled jobs.

### Resource Limits

Add resource limits to `docker-compose.yml`:

```yaml
services:
  web:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 512M
```

## Deployment

### Cloud Platforms

#### Heroku

```bash
# Not recommended - Heroku doesn't support docker-compose
# Use their container registry instead
```

#### DigitalOcean App Platform

1. Connect your GitHub repository
2. Select "Docker Compose" as build type
3. Configure environment variables
4. Deploy

#### AWS ECS

1. Push images to ECR
2. Create task definitions for web and worker
3. Configure ALB for web service
4. Deploy services

## Backup and Restore

### Backup Database

```bash
# Copy database from volume
docker compose exec web sqlite3 /app/data/t38_email.db .dump > backup.sql

# Or copy the entire volume
docker run --rm -v t38-planning-aid-website_db_data:/data -v $(pwd):/backup alpine tar czf /backup/db_backup.tar.gz -C /data .
```

### Restore Database

```bash
# Stop services
docker compose down

# Restore from backup
docker run --rm -v t38-planning-aid-website_db_data:/data -v $(pwd):/backup alpine tar xzf /backup/db_backup.tar.gz -C /data

# Start services
docker compose up -d
```

## Security Best Practices

1. **Never commit `.env` file** - Contains sensitive credentials
2. **Use app passwords** - For Gmail, use App Passwords not your main password
3. **Run as non-root** - Dockerfile uses `appuser` (UID 1000)
4. **Read-only volumes** - Parent repo mounted as read-only
5. **Health checks** - Services monitored and auto-restart on failure
6. **Network isolation** - Services communicate via dedicated network

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)
- [APScheduler Documentation](https://apscheduler.readthedocs.io/)

## Support

For issues or questions:
1. Check logs: `docker compose logs -f`
2. Review this documentation
3. Check `README.md` for general setup
4. See `DEPLOYMENT.md` for deployment guides
